"""
Job Scraper Django Integration
Adds job scraping functionality to the Django contact management system.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import asyncio
import logging
from typing import Dict, List
import json
import sys
import platform

# Fix for Windows subprocess issue with Playwright
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from services.job_scraper import JobScraper
from services.scraping_exceptions import ScrapingError

logger = logging.getLogger(__name__)


def run_scraper_async(scraper, url):
    """
    Helper function to run scraper with Windows-compatible event loop.
    """
    if platform.system() == 'Windows':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(scraper.scrape_jobs(url))
        finally:
            loop.close()
    else:
        return asyncio.run(scraper.scrape_jobs(url))


@login_required
def job_scraper_view(request):
    """
    Main job scraper interface.
    """
    if request.method == 'POST':
        url = request.POST.get('url', '').strip()
        
        if not url:
            messages.error(request, 'Please provide a valid URL')
            return render(request, 'jobs/scraper.html')
        
        try:
            # Run scraper asynchronously
            scraper = JobScraper()
            jobs = run_scraper_async(scraper, url)
            
            # Store results in session for display
            request.session['scraped_jobs'] = jobs
            request.session['scraped_url'] = url
            
            messages.success(request, f'Successfully scraped {len(jobs)} jobs from {url}')
            return redirect('jobs:results')
            
        except ScrapingError as e:
            logger.error(f"Scraping error: {e}")
            messages.error(request, f'Scraping failed: {str(e)}')
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            messages.error(request, f'An unexpected error occurred: {str(e)}')
    
    return render(request, 'jobs/scraper.html')


@login_required
def job_results_view(request):
    """
    Display scraped job results.
    """
    jobs = request.session.get('scraped_jobs', [])
    url = request.session.get('scraped_url', '')
    
    if not jobs:
        messages.warning(request, 'No job data found. Please scrape a website first.')
        return redirect('jobs:scraper')
    
    context = {
        'jobs': jobs,
        'url': url,
        'job_count': len(jobs)
    }
    
    return render(request, 'jobs/results.html', context)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def job_scraper_api(request):
    """
    API endpoint for job scraping.
    """
    try:
        data = json.loads(request.body)
        url = data.get('url', '').strip()
        
        if not url:
            return JsonResponse({
                'success': False,
                'error': 'URL is required'
            }, status=400)
        
        # Run scraper
        scraper = JobScraper()
        jobs = run_scraper_async(scraper, url)
        
        return JsonResponse({
            'success': True,
            'jobs': jobs,
            'count': len(jobs),
            'url': url
        })
        
    except ScrapingError as e:
        logger.error(f"Scraping error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'An unexpected error occurred'
        }, status=500)


@login_required
def job_scraper_status(request):
    """
    Get scraping status and configuration.
    """
    config = {
        'timeouts': {
            'page_load': 30,
            'popup_detection': 5,
            'scroll_wait': 2,
            'content_load': 10,
        },
        'retries': {
            'popup_dismissal': 3,
            'button_click': 3,
            'scroll_iteration': 50,
        },
        'selectors': {
            'popup': '.top-level-modal-container',
            'close_button': 'button.close, button[aria-label="Close"]',
            'job_card': '.job-card, .job-item',
            'more_button': 'button:has-text("See more jobs")',
        },
        'delays': {
            'after_popup': 1,
            'after_scroll': 1,
            'after_click': 2,
        }
    }
    
    return JsonResponse({
        'status': 'ready',
        'config': config,
        'features': [
            'Popup handling',
            'Infinite scrolling',
            'Button detection',
            'Job extraction',
            'Error handling',
            'Logging'
        ]
    })


def test_scraper(request):
    """
    Test endpoint for scraping functionality.
    """
    if request.method == 'POST':
        test_url = request.POST.get('test_url', 'https://example.com')
        
        try:
            scraper = JobScraper()
            jobs = run_scraper_async(scraper, test_url)
            
            return JsonResponse({
                'success': True,
                'message': f'Test completed successfully. Found {len(jobs)} jobs.',
                'jobs': jobs[:5] if jobs else [],  # Show first 5 jobs
                'total_count': len(jobs)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return render(request, 'jobs/test.html')

