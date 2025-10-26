<!DOCTYPE html>
<html>
<head>
    <title>Contacts</title>
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <style>
        body { font-family: Arial; margin: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #ddd; padding: 8px; }
        th { background: #f4f4f4; }
        .pagination { margin-top: 15px; display: flex; justify-content: center; }
        select, input { margin-right: 10px; padding: 5px; }
    </style>

    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <!-- Select2 -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.1.0-rc.0/css/select2.min.css" rel="stylesheet"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.1.0-rc.0/js/select2.min.js"></script>
</head>
<body>
<div class="container">
<form
        class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search" action="{{route('contact.index')}}" method="get">
        <div class="input-group">
            <input type="text" class="form-control bg-light border-0  small" id="apolloUrl" name="global_search" placeholder="Search for..."
                aria-label="Search" aria-describedby="basic-addon2">
            <div class="input-group-append">
			<input type="submit" class="btn btn-primary" id="goApolloBtn">
                
            </div>
        </div>
    </form>
    <h3>Contacts (Total: {{ number_format($totalCount) }})</h3>

    <!-- Filters -->
    <div style="display:flex; flex-wrap:wrap; gap:10px; margin-bottom:15px; align-items:center;">
        <input type="text" id="name" placeholder="Name" style="width:200px;" />
        <select id="job_title" multiple="multiple" style="width:220px;" placeholder="Job Title"></select>
        <select id="industry" multiple="multiple" style="width:220px;" placeholder="Industry"></select>
        <select id="technology" multiple="multiple" style="width:220px;" placeholder="Technologies"></select>
        <select id="location" multiple="multiple" style="width:220px;" placeholder="Location"></select>

        <select id="employees" multiple="multiple" style="width:180px;" placeholder="Employees">
            @php
                $ranges = ['1-10','11-20','21-50','51-100','101-200','201-500','501-1000','1001-2000','2001-5000','5001-10000','10001+'];
            @endphp
            @foreach($ranges as $range)
                <option value="{{ $range }}">{{ $range }}</option>
            @endforeach
        </select>

        <select id="email_status" multiple="multiple" style="width:180px;" placeholder="Email Status">
            @foreach(['Verified','Unverified','Guessed','User Managed','New Data Available','N/A'] as $status)
                <option value="{{ $status }}">{{ $status }}</option>
            @endforeach
        </select>

        <input type="number" id="min_rev" placeholder="Min Rev" style="width:120px;" />
        <input type="number" id="max_rev" placeholder="Max Rev" style="width:120px;" />
        <input type="text" id="linkedin" placeholder="LinkedIn URL" style="width:220px;" />
    </div>

    <!-- Results table -->
    <div id="contactsTable">
        @include('contact.partials.table', ['contacts' => $contacts])
    </div>
</div>
<script>
$(function(){
    // ----------------------------
    // Variables
    // ----------------------------
    let currentRequest = null;
    let debounceTimer = null;

    // ----------------------------
    // AJAX fetch function
    // ----------------------------
    function fetchContacts(page = 1) {
        const payload = {
            name: $('#name').val(),
            job_title: $('#job_title').val(),
            industry: $('#industry').val(),
            technology: $('#technology').val(),
            location: $('#location').val(),
            employees: $('#employees').val(),
            email_status: $('#email_status').val(),
            min_rev: $('#min_rev').val(),
            max_rev: $('#max_rev').val(),
            linkedin: $('#linkedin').val(),
            page: page
        };

        if (currentRequest) currentRequest.abort();

        currentRequest = $.ajax({
            url: "{{ route('contact.index') }}",
            data: payload,
            beforeSend: function() { $('#contactsTable').html('<p>Loading...</p>'); },
            success: function(html) { $('#contactsTable').html(html); },
            error: function(xhr, status) {
                if (status !== 'abort') $('#contactsTable').html('<p style="color:red;">Error loading data</p>');
            },
            complete: function() { currentRequest = null; }
        });
    }
$('#goApolloBtn').on('click', function(){
  let apolloUrl = $('#apolloUrl').val().trim();
  if (!apolloUrl) { alert('Please paste an Apollo URL.'); return; }

  const target = `"{{ route('contact.index') }}?global_search=" + encodeURIComponent(apolloUrl)`;
  window.location.href = target;
});
const gs = new URLSearchParams(window.location.search).get('global_search');
if (gs) {
   const decoded = decodeURIComponent(gs);
   // Now manually set window.location.hash = the part after `#` in decoded, if needed
   const hashIndex = decoded.indexOf('#');
   if (hashIndex >= 0) {
     window.location.hash = decoded.substr(hashIndex + 1);
   }
   // Then parse parameters from decoded (before `#`) + from hash using your existing parse function
}

    // ----------------------------
    // Parse Apollo URL (query + hash)
    // ----------------------------
    function parseApolloEncodedParam() {
        const params = {};

        // Query string (?key=value&...)
        const search = window.location.search.substring(1);
        if (search) {
            const searchParams = new URLSearchParams(search);
            searchParams.forEach((v, k) => {
                const key = k.replace(/\[\]$/,'');
                if (params[key]) params[key] = [].concat(params[key], v);
                else params[key] = v;
            });
        }

        // Hash fragment (#/people?key=value&...)
        const hash = window.location.hash;
        if (hash.includes('?')) {
            const fragmentQuery = hash.split('?')[1];
            const fragParams = new URLSearchParams(fragmentQuery);
            fragParams.forEach((v, k) => {
                const key = k.replace(/\[\]$/,'');
                if (params[key]) params[key] = [].concat(params[key], v);
                else params[key] = v;
            });
        }

        return params;
    }

    const apolloParams = parseApolloEncodedParam();
    console.log('Parsed Apollo Params:', apolloParams);

    // ----------------------------
    // Setup Select2 AJAX
    // ----------------------------
    function createAjaxSelect(id, type) {
        $('#' + id).select2({
            placeholder: $('#' + id).attr('placeholder') || id,
            allowClear: true,
            multiple: true,
            ajax: {
                url: "{{ route('filter.options') }}",
                dataType: 'json',
                delay: 400,
                data: function(params) { return { term: params.term || '', type: type }; },
                processResults: function(data) { return data; },
                cache: true
            },
            width: 'resolve'
        });
    }

    $('#employees, #email_status').select2({ placeholder: 'Select', allowClear:true, width:'resolve' });

    createAjaxSelect('job_title', 'job_title');
    createAjaxSelect('industry', 'industry');
    createAjaxSelect('technology', 'technology');
    createAjaxSelect('location', 'location');

    // ----------------------------
    // Prefill function
    // ----------------------------
  function setMultiWithText(id, values, type) {
    if (!values) return Promise.resolve();
    const arr = Array.isArray(values) ? values : [values];
    const select = $('#' + id);

    const promises = arr.map(v => {
        if (!v) return Promise.resolve();
        if (select.find("option[value='" + v + "']").length === 0) {
            // Fetch the text from backend
            return $.ajax({
                url: "{{ route('filter.options') }}",
                dataType: 'json',
                data: { type: type, id: v },
            }).then(data => {
                if (data.results.length) {
                    const option = new Option(data.results[0].text, data.results[0].id, true, true);
                    select.append(option).trigger('change');
                }
            });
        } else {
            select.find("option[value='" + v + "']").prop('selected', true);
            select.trigger('change');
            return Promise.resolve();
        }
    });

    return Promise.all(promises);
}


    function setMulti(id, values) {
        if (!values) return;
        const arr = Array.isArray(values) ? values : [values];
        const select = $('#' + id);

        arr.forEach(v => {
            if (!v) return;
            if (select.find("option[value='" + v + "']").length === 0) {
                const newOption = new Option(v, v, true, true);
                select.append(newOption);
            } else {
                select.find("option[value='" + v + "']").prop('selected', true);
            }
        });

        select.trigger('change');
    }

    async function prefillFromApollo() {
    const map = apolloParams;
    console.log('Apollo Params:', map);

    // Job Titles
    const jobKeys = ['personTitles','personSeniorities'];
    for (const k of jobKeys) if (map[k]) setMulti('job_title', map[k]);

    // Technology
    if (map['technologies'] || map['keywords']) setMulti('technology', map['technologies'] || map['keywords']);

    // Location
    if (map['personLocations']) setMulti('location', map['personLocations']);

    // Email Status
    if (map['contactEmailStatusV2']) setMulti('email_status', map['contactEmailStatusV2']);

    // Employees
    // Employees
let empRanges = map['organizationNumEmployeesRanges'] || map['organizationNumEmployeesRanges[]'];
if (empRanges) {
    // Ensure it's an array
    if (!Array.isArray(empRanges)) empRanges = [empRanges];

    // Convert "1,10" -> "1-10"
    const formatted = empRanges.map(v => v.replace(',', '-'));
    setMulti('employees', formatted);
}


    // Industry (await completion)
    if (map['organizationIndustryTagIds']) {
        await setMultiWithText('industry', map['organizationIndustryTagIds'], 'industry');
    }

    // After all prefill
    fetchContacts();

    console.log('--- Final Select2 Values ---');
    console.log('Job Titles:', $('#job_title').val());
    console.log('Industry:', $('#industry').val());
    console.log('Technologies:', $('#technology').val());
    console.log('Locations:', $('#location').val());
    console.log('Email Status:', $('#email_status').val());
    console.log('Employees:', $('#employees').val());
}


    // Run prefill
    prefillFromApollo();

    // ----------------------------
    // Event bindings
    // ----------------------------
    $('#name, #min_rev, #max_rev, #linkedin').on('keyup', function(){
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(()=>fetchContacts(), 450);
    });

    $('#job_title, #industry, #technology, #employees, #email_status,#location').on('change', function(){
        fetchContacts();
    });

    $(document).on('click', '.pagination a', function(e){
        e.preventDefault();
        const page = $(this).attr('href').split('page=')[1] || 1;
        fetchContacts(page);
    });
});
</script>



</body>
</html>
