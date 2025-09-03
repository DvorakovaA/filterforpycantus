from urllib.parse import quote

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import FilterForm

from filter.construct_file import construct_yaml

def index(request):
    if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            # Custom logic for dynamic fields
            def collect_dynamic_field(name):
                i = 0
                values = []
                while f"{name}_{i}" in request.POST:
                    val = request.POST.get(f"{name}_{i}")
                    if val == 'other':
                        custom_val = request.POST.get(f"{name}_other_{i}", '').strip()
                        if custom_val:
                            values.append(custom_val)
                    elif val:
                        values.append(val)
                    i += 1
                return list(set(values))

            request.session['form_data'] = {'name' : form.cleaned_data['name'],
                                            'genre_incl' : collect_dynamic_field("genre_incl"),
                                            'office_incl' : collect_dynamic_field("office_incl"),
                                            'feast_incl' : collect_dynamic_field("feast_incl"),
                                            'db_incl' : collect_dynamic_field("db_incl"),
                                            'siglum_incl' : collect_dynamic_field("siglum_incl"),
                                            'title_incl' : collect_dynamic_field("title_incl"),
                                            'provenance_incl' : collect_dynamic_field("provenance_incl"),
                                            'century_incl' : collect_dynamic_field("century_incl"),
                                            'num_century_incl' : collect_dynamic_field("num_century_incl"),
                                            'cursus_incl' : collect_dynamic_field("cursus_incl"),
                                            'genre_excl' : collect_dynamic_field("genre_excl"),
                                            'office_excl' : collect_dynamic_field("office_excl"),
                                            'feast_excl' : collect_dynamic_field("feast_excl"),
                                            'db_excl' : collect_dynamic_field("db_excl"),
                                            'siglum_excl' : collect_dynamic_field("siglum_excl"),
                                            'title_excl' : collect_dynamic_field("title_excl"),
                                            'provenance_excl' : collect_dynamic_field("provenance_excl"),
                                            'century_excl' : collect_dynamic_field("century_excl"),
                                            'num_century_excl' : collect_dynamic_field("num_century_excl"),
                                            'cursus_excl' : collect_dynamic_field("cursus_excl")}
            return redirect('download')
    else:
        form = FilterForm()

    return render(request, 'filter/index.html', {'form': form})



def download(request):
    form_data = request.session.get('form_data')

    if not form_data:
        return JsonResponse({'error': 'No form data found'}, status=404)

    # If user clicked the "Download" button
    if request.GET.get('download') == '1':
        filename, yaml_content = construct_yaml(form_data)
        response = HttpResponse(yaml_content, content_type='application/x-yaml; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{quote(filename+".yaml")}"'
        return response

    return render(request, 'filter/download.html', {'form_data': form_data})


def help(request):
    """
    Function that manages displaying of help page
    """
    return render(request, "filter/help.html")


def about(request):
    """
    Function that manages displaying of about page
    """
    return render(request, "filter/about.html")

def contact(request):
    """
    Function that manages displaying of contact page
    """
    return render(request, "filter/contact.html")