<table border="1" width="100%" cellspacing="0" cellpadding="5">
    <thead>
        <tr>
            <th>Sno</th>
            <th>Name</th>
            <th>Linkedin</th>
            <th>Email Status</th>
            <th>Job Title</th>
            <th>Industry</th>
            <th>Location</th>
            <th>Technologies</th>
            <th>Annual revenue</th>
        </tr>
    </thead>
    <tbody>
    @forelse ($contacts as $contact)
        <tr>
            <td>{{ $loop->iteration }}</td>
            <td>{{ $contact->first_name }} {{ $contact->last_name }}</td>
            <td>{{ $contact->person_linkedin_url }}</td>
            <td>{{ $contact->email_status }}</td>
            <td>{{ $contact->title }}</td>
            <td>{{ $contact->industry }}</td>
            <td>{{ $contact->city }}, {{ $contact->state }}, {{ $contact->country }}</td>
            <td>{{ $contact->technologies }}</td>
            <td>{{ $contact->annual_revenue }}</td>
        </tr>
    @empty
        <tr><td colspan="5" style="text-align:center;">No results found</td></tr>
    @endforelse
    </tbody>
</table>

<div style="margin-top:15px;">
    {!! $contacts->links() !!}
</div>
