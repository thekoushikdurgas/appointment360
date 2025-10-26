<div class="card mb-3">
    <div class="card-header">
        <h5>Filter Contacts</h5>
    </div>
    <div class="card-body">
        <form method="GET" action="{{ route('contacts.index') }}">
            <div class="row g-2">
                <div class="col-md-4">
                    <input type="text" name="name" class="form-control" placeholder="Name" value="{{ request('name') }}">
                </div>
                <div class="col-md-4">
                    <input type="text" name="location" class="form-control" placeholder="Location" value="{{ request('location') }}">
                </div>
                <div class="col-md-4">
                    <button type="submit" class="btn btn-primary w-100">Filter</button>
                </div>
            </div>
        </form>
    </div>
</div>
