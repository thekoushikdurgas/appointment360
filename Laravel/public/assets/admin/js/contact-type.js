var cDataTable;

$(document).ready(function () {
    console.log(serverUrl);
//    $("#contact_type_table").dataTable({
//          "searching": false,
//            "lengthChange": false,
//            "info":     false,
//        scrollCollapse: true,
//       
//    scrollY: '300px'});
//     $(".parcel-type-menu-link").addClass("active");
//    cDataTable= $("#contact_type_table").dataTable({
//        "searching": false,
//        "lengthChange": false,
//        "info": false,
//        scrollCollapse: true,
//        scrollY: '300px',
//        serverSide: true,
//        processing: true,
//        "ajax": {
//            url: serverUrl + "contacts/ajax-data",
//            type: "POST",
//            headers: {
//                "X-CSRF-TOKEN": requestToken,
//            },
////            data: {
////                search_keyword: '',
////                search_column: ''
////                
////            },
//            //"dataType": "json",
//        },
//        
//        "columns": [
//            {"data": "id", "name": "id"},
//            {"data": "name", "name": "name"},
//            {"data": "title", "name": "title"},
//            {"data": "company", "name": "company"},
//            {"data": "quick_actions", "name": "quick_actions"},
//            {"data": "contact_location", "name": "contact_location"},
//            {"data": "no_employees", "name": "no_employees"},
//            {"data": "phone", "name": "phone"},
//            {"data": "industry", "name": "industry"},
//            {"data": "keywords", "name": "keywords"},
//        ],
//
//    });
//
//
//    
//    $(document).on("click", ".contacts_delete", function (e){
//        var data = {
//            message: "You won't be able to revert this!",
//            slug: 'contacts',
//            datatable_id: 'parcel_type_table'
//        };
//        deleteRecordConfirmBox( this, e, data );
//        
//          
//    })
//    
//
});
$(document).ready(function () {


    $('.js-example-basic-single').select2({

        placeholder: "select...",
        ajax: {
            type: "POST",
            dataType: 'json',
            url: serverUrl + "contacts/ajax-select",
            //url: 'search_employees',        
            processResults: function (data) {
                console.log(data);
                if (data.length == 0)
                    $('.js-example-basic-single').val(null).trigger('change');
                return {
                    results: $.map(data, function (obj) {
                        return {id: obj.title, text: obj.title};
                    })
                };
            },
            data: function (params) {
                intializeTable(params.term, 'title');

                return {search_keyword: params.term, search_column: "title", "_token": requestToken, }
            }
        }
    });

    $('.js-company').select2({

        placeholder: "select...",
        ajax: {
            type: "POST",
            dataType: 'json',
            url: serverUrl + "contacts/ajax-select",
            //url: 'search_employees',        
            processResults: function (data) {
                //console.log(data);
                if (data.length == 0)
                    $('.js-company').val(null).trigger('change');
                return {
                    results: $.map(data, function (obj) {
                        return {id: obj.company, text: obj.company};
                    })
                };

            },
            data: function (params) {
                intializeTable(params.term, 'company');

                return {search_keyword: params.term, search_column: "company", "_token": requestToken, }
            }
        }
    });
    $('.js-industry').select2();
    $('.js-keywords').select2({

        placeholder: "select...",
        ajax: {
            type: "POST",
            dataType: 'json',
            url: serverUrl + "contacts/ajax-select",
            //url: 'search_employees',        
            processResults: function (data) {
                console.log(data);
                if (data.length == 0)
                    $('.js-keywords').val(null).trigger('change');
                return {
                    results: $.map(data, function (obj) {
                        return {id: obj, text: obj};
                    })
                };

            },
            data: function (params) {
                intializeTable(params.term, 'keywords');

                return {search_keyword: params.term, search_column: "keywords", "_token": requestToken, }
            }
        }
    });
    $('.js-technologies').select2({

        placeholder: "select...",
        ajax: {
            type: "POST",
            dataType: 'json',
            url: serverUrl + "contacts/ajax-select",
            //url: 'search_employees',        
            processResults: function (data) {
                console.log(data);
                if (data.length == 0)
                    $('.js-technologies').val(null).trigger('change');
                return {
                    results: $.map(data, function (obj) {
                        return {id: obj, text: obj};
                    })
                };



            },
            data: function (params) {
                intializeTable(params.term, 'technologies');

                return {search_keyword: params.term, search_column: "technologies", "_token": requestToken, }
            }
        }
    });
    $('.js-location').select2({

        placeholder: "select...",
        ajax: {
            type: "POST",
            dataType: 'json',
            url: serverUrl + "contacts/ajax-select",
            //url: 'search_employees',        
            processResults: function (data) {
                console.log(data);
                if (data.length == 0)
                    $('.js-location').val(null).trigger('change');
                return {
                    results: $.map(data, function (obj) {
                        return {id: obj.location, text: obj.location};
                    })
                };



            },
            data: function (params) {
                intializeTable(params.term, 'company_address');

                return {search_keyword: params.term, search_column: "company_address", "_token": requestToken, }
            }
        }
    });



    $('.js-example-basic-single').on('select2:select', function (e) {
        //console.log("select done", e.params);
        var ids = [];
        $.map($('.js-example-basic-single').select2('data'), function (obj) {
            ids.push(obj.id); // replace pk with your identifier

        });
        // console.log(ids.join());
        intializeTable(ids.join(), 'title');
    });
    $('.js-company').on('select2:select', function (e) {
        console.log("select done", e.params);
        var ids = [];
        $.map($('.js-company').select2('data'), function (obj) {
            ids.push(obj.id); // replace pk with your identifier

        });
        // console.log(ids.join());
        intializeTable(ids.join(), 'company');
    });
    
    $('.js-keywords').on('select2:select', function (e) {
        console.log("select done", e.params);
        var ids = [];
        $.map($('.js-keywords').select2('data'), function (obj) {
            ids.push(obj); // replace pk with your identifier

        });
        // console.log(ids.join());
        intializeTable(ids.join(), 'keywords');
    });
    $('.js-technologies').on('select2:select', function (e) {
        console.log("select done", e.params);
        var ids = [];
        $.map($('.js-technologies').select2('data'), function (obj) {
            ids.push(obj); // replace pk with your identifier

        });
        // console.log(ids.join());
        intializeTable(ids.join(), 'technologies');
    });
    $('.js-location').on('select2:select', function (e) {
        console.log("select done", e.params);
        var ids = [];
        $.map($('.js-location').select2('data'), function (obj) {
            ids.push(obj.id); // replace pk with your identifier

        });
        // console.log(ids.join());
        intializeTable(ids.join(), 'company_address');
    });






//    $('.js-example-basic-single').select2().on('change', function () {
//        let inventoryId = $(this).val();
//        alert("changed");
//        $.ajax({
//            type: "POST",
//            data: {
//                search_keyword: inventoryId,
//                search_column: 'title',
//                _token: requestToken
//            },
//            url: serverUrl + "contacts/ajax-data",
//            success: function (response) {
//                $(".js-example-basic-single").select2({
//                    data: response
//                });
//            }
//        });
//
//    });


intializeTable('', '');

    function intializeTable(searchterm, searchcolumn) {
		var job_titles= $('#job_titles').val();
		var name_search= $('#name_search').val();
		$('#headingTwo .name-title').html(name_search);
		$('#headingThree .job-title').html(job_titles);
        $('#contact_type_table').DataTable({
            destroy: true,
            processing: true,
            serverSide: true,
            scrollY: 320,
            scrollX: true,
            "searching": false,
            "lengthChange": false,
            "info": true,
            scrollCollapse: true,
            ajax: {
                type: "post",
                url: serverUrl + "contacts/ajax-data",
                data: {
					contactEmailStatusV2: $('.email_status:checked').map(function(){return $(this).val()}).get(),
					employess_range: $('.employess_range:checked').map(function(){return $(this).val()}).get(),
                    job_titles: $('#job_titles').val(),
                    js_technologies: $('.js-technologies').val(),
                    js_company: $('.js-company').val(),
                    js_industry: $('.js-industry').val(),
                    name_search: $('#name_search').val(),
                    min_rev: $('#min-rev').val(),
                    max_rev: $('#max-rev').val(),
                    search_location: $('#search_location').val(),
                    search_linkedin: $('#search_linkedin').val(),
                    _token: requestToken
                }, },

            "columns": [

                {"data": "name", "name": "name"},
                {"data": "title", "name": "title"},
                {"data": "company", "name": "company"},
                {"data": "quick_actions", "name": "quick_actions"},
                {"data": "contact_location", "name": "contact_location"},
                {"data": "no_employees", "name": "no_employees"},
                {"data": "phone", "name": "phone"},
                {"data": "industry", "name": "industry"},
                {"data": "keywords", "name": "keywords"},
            ]

        });

    }



    $('.collapse.in').prev('.panel-heading').addClass('active');
    $('#accordion, #bs-collapse')
            .on('show.bs.collapse', function (a) {
                $(a.target).prev('.panel-heading').addClass('active');
            })
            .on('hide.bs.collapse', function (a) {
                $(a.target).prev('.panel-heading').removeClass('active');
            });
    $("#name_search").keyup(function () {
        var name_search = $("#name_search").val();
        intializeTable(name_search, 'first_name');
    });
	
	$("#search_linkedin").keyup(function () {
        var search_linkedin = $("#search_linkedin").val();
        intializeTable(search_linkedin, 'search_linkedin');
    }); 

	$("#search_location").keyup(function () {
        var search_location = $("#search_location").val();
        intializeTable(search_location, 'search_location');
    });
  
    $("#min-rev").change(function () {
        var min_rev = $("#min-rev").val();
        var max_rev = $("#max-rev").val();

        if (max_rev != '') {
            min_rev = min_rev + "_to_" + max_rev
        }
        intializeTable(min_rev, 'annual_revenue');
    });
    $("#max-rev").change(function () {
        var max_rev = $("#max-rev").val();
        var min_rev = $("#min-rev").val();
        if (min_rev != '') {
            max_rev = min_rev + "_to_" + max_rev
        }

        intializeTable(max_rev, 'annual_revenue');
    });
    
    $('input.email_status').bind('click', function () {
      
            var idsComenzi = [];

            $('input.email_status:checked').each(function () {
                idsComenzi.push($(this).val());
            });
            intializeTable(idsComenzi, 'email_status');
        
    });
    $('input.employess_range').bind('click', function () {
      
            var idsComenzi = [];

            $('input.employess_range:checked').each(function () {
                idsComenzi.push($(this).val());
            });
            intializeTable(idsComenzi, 'employees');
        
    });
});