"""
Background Job Service - Handle import jobs in background with progress tracking
"""
import threading
import time
from datetime import datetime
from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from models.import_job import ImportJob
from services.spark_import_service import SparkImportService
from services.bulk_insert_service import BulkInsertService
from config.database import get_db
import os


class BackgroundJobService:
    """Manage background import jobs with progress tracking"""
    
    def __init__(self):
        self.jobs = {}  # job_id -> thread
        self.job_threads = {}  # job_id -> Thread object
        
    def create_import_job(self, db: Session, filename: str, file_path: str, 
                         column_mapping: Dict, user_id: int = 1, is_local_file: bool = False) -> ImportJob:
        """Create a new import job in database"""
        # Get file size
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        
        # Create job record
        job = ImportJob(
            user_id=user_id,
            filename=filename,
            file_size=file_size,
            status="PENDING",
            started_at=None,
            column_mapping=str(column_mapping)
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        
        return job
    
    def start_import_job(self, job_id: int, file_path: str, column_mapping: Dict):
        """Start import job in background thread"""
        if job_id in self.job_threads:
            # Job already running
            return
        
        # Create background thread
        thread = threading.Thread(
            target=self._run_import_job,
            args=(job_id, file_path, column_mapping),
            daemon=True
        )
        
        self.job_threads[job_id] = thread
        thread.start()
    
    def _run_import_job(self, job_id: int, file_path: str, column_mapping: Dict):
        """Execute import job in background"""
        db = next(get_db())
        
        try:
            # Get job from database
            job = db.query(ImportJob).filter(ImportJob.id == job_id).first()
            if not job:
                return
            
            # Update status to processing
            job.status = "PROCESSING"
            job.started_at = datetime.utcnow()
            db.commit()
            
            # Initialize services
            spark_service = SparkImportService()
            bulk_service = BulkInsertService(db)
            
            # Process import
            results = spark_service.process_import(file_path, column_mapping)
            
            job.total_rows = results['total_rows']
            job.total_batches = len(results['batches'])
            
            # Process batches
            total_success = 0
            total_errors = 0
            
            for i, batch_df in enumerate(results['batches']):
                # Update progress
                job.current_batch = i + 1
                job.processed_rows = int((i + 1) / job.total_batches * results['valid_rows'])
                
                # Calculate speed
                elapsed = (datetime.utcnow() - job.started_at).total_seconds()
                if elapsed > 0:
                    job.processing_speed = job.processed_rows / elapsed
                
                # Estimate completion
                if job.processing_speed > 0:
                    remaining_rows = results['valid_rows'] - job.processed_rows
                    remaining_seconds = remaining_rows / job.processing_speed
                    job.estimated_completion = datetime.utcnow().timestamp() + remaining_seconds
                
                # Insert batch
                batch_results = bulk_service.bulk_insert_from_dataframe(batch_df, job.user_id)
                total_success += batch_results['success_count']
                total_errors += batch_results['error_count']
                
                # Update job progress
                job.success_count = total_success
                job.error_count = total_errors
                db.commit()
                
                # Check for cancellation
                db.refresh(job)
                if job.status == "CANCELLED":
                    break
            
            # Complete job
            job.status = "COMPLETED" if job.status != "CANCELLED" else "CANCELLED"
            job.completed_at = datetime.utcnow()
            job.processed_rows = results['valid_rows']
            job.success_count = total_success
            job.error_count = total_errors
            
            # Calculate final statistics
            if job.started_at:
                total_time = (job.completed_at - job.started_at).total_seconds()
                if total_time > 0:
                    job.processing_speed = job.processed_rows / total_time
            
            db.commit()
            
        except Exception as e:
            # Mark job as failed
            db.refresh(job)
            job.status = "FAILED"
            job.completed_at = datetime.utcnow()
            job.error_log = str(e)
            db.commit()
            
            print(f"Import job {job_id} failed: {str(e)}")
        
        finally:
            db.close()
            # Remove from active jobs
            if job_id in self.job_threads:
                del self.job_threads[job_id]
    
    def get_job_status(self, job_id: int) -> Optional[Dict]:
        """Get current status of import job"""
        db = next(get_db())
        
        try:
            job = db.query(ImportJob).filter(ImportJob.id == job_id).first()
            if not job:
                return None
            
            return {
                'id': job.id,
                'status': job.status,
                'filename': job.filename,
                'total_rows': job.total_rows,
                'processed_rows': job.processed_rows,
                'success_count': job.success_count,
                'error_count': job.error_count,
                'duplicate_count': job.duplicate_count,
                'progress_percentage': job.get_progress_percentage(),
                'processing_speed': job.processing_speed,
                'current_batch': job.current_batch,
                'total_batches': job.total_batches,
                'started_at': job.started_at.isoformat() if job.started_at else None,
                'completed_at': job.completed_at.isoformat() if job.completed_at else None,
                'estimated_completion': job.estimated_completion,
                'is_complete': job.is_complete(),
                'is_running': job.is_running()
            }
        finally:
            db.close()
    
    def cancel_job(self, job_id: int) -> bool:
        """Cancel a running import job"""
        db = next(get_db())
        
        try:
            job = db.query(ImportJob).filter(ImportJob.id == job_id).first()
            if not job:
                return False
            
            if job.status in ['PENDING', 'PROCESSING']:
                job.status = "CANCELLED"
                job.completed_at = datetime.utcnow()
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def get_recent_jobs(self, user_id: int = None, limit: int = 10) -> List[Dict]:
        """Get list of recent import jobs"""
        db = next(get_db())
        
        try:
            query = db.query(ImportJob)
            
            if user_id:
                query = query.filter(ImportJob.user_id == user_id)
            
            jobs = query.order_by(ImportJob.created_at.desc()).limit(limit).all()
            
            return [{
                'id': job.id,
                'filename': job.filename,
                'status': job.status,
                'total_rows': job.total_rows,
                'success_count': job.success_count,
                'error_count': job.error_count,
                'progress_percentage': job.get_progress_percentage(),
                'created_at': job.created_at.isoformat() if job.created_at else None,
                'completed_at': job.completed_at.isoformat() if job.completed_at else None
            } for job in jobs]
        finally:
            db.close()

