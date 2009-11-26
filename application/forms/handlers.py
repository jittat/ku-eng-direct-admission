# -*- coding: utf-8 -*-

from django.conf import settings

from application.models import Major, MajorPreference
from application.models import Address, ApplicantAddress
from application.forms import EducationForm, PersonalInfoForm
from application.forms import AddressForm

def extract_ranks(post_data, major_list):
    """
    extracts a list of majors from post data.  Each select list has an
    id of the form 'major_ID'.
    """
    
    rank_dict = {}
    for m in major_list:
        sel_id = m.select_id()
        if sel_id in post_data:
            r = post_data[sel_id]
            try:
                rnum = int(r)
            except:
                rnum = -1
            if (rnum >= 1) and (rnum <= settings.MAX_MAJOR_RANK):
                rank_dict[rnum] = int(m.number)

    ranks = []
    for r in sorted(rank_dict.keys()):
        ranks.append(rank_dict[r])
    return ranks


def handle_major_form(request):
    applicant = request.applicant
    majors = Major.get_all_majors()

    errors = None

    #print extract_ranks(request.POST, majors)

    major_ranks = extract_ranks(request.POST, majors)
    if len(major_ranks)==0:
        # chooses no majors
        errors = ['ต้องเลือกอย่างน้อยหนึ่งอันดับ']
    else:
        if applicant.has_major_preference():
            preference = applicant.preference
        else:
            preference = MajorPreference()
            
        preference.majors = major_ranks

        preference.applicant = applicant
        preference.save()
        applicant.add_related_model('major_preference',
                                    save=True,
                                    smart=True)

        return (True, major_ranks, None)

    return (False, major_ranks, errors)


def handle_basic_form_save(form_class, field_name, request, old_data, 
                           applicant=None):
    if applicant==None:
        applicant = request.applicant
    if (request.method == 'POST') and ('cancel' not in request.POST):
        form = form_class(request.POST, 
                          instance=old_data)
        if form.is_valid():
            data = form.save(commit=False)
            data.applicant = applicant
            data.save()
            applicant.add_related_model(field_name,
                                        save=True,
                                        smart=True)
            return (True, form)
    else:
        form = form_class(instance=old_data)
    return (False, form)


def handle_personal_info_form(request, old_info, applicant=None):
    return handle_basic_form_save(PersonalInfoForm,
                                  'personal_info',
                                  request,
                                  old_info,
                                  applicant)

def handle_education_form(request, old_education, applicant=None):
    return handle_basic_form_save(EducationForm,
                                  'educational_info',
                                  request,
                                  old_education,
                                  applicant)


def handle_address_form(request, applicant=None):
    if applicant==None:
        applicant = request.applicant

    have_old_address = applicant.has_address()

    if have_old_address:
        old_applicant_address = applicant.address
        old_home_address = applicant.address.home_address
        old_contact_address = applicant.address.contact_address
    else:
        # still need this for form instances
        old_home_address, old_contact_address = None, None

    if (request.method == 'POST') and ('cancel' not in request.POST):

        home_address_form = AddressForm(request.POST, 
                                        prefix="home",
                                        instance=old_home_address)
        contact_address_form = AddressForm(request.POST, 
                                           prefix="contact",
                                           instance=old_contact_address)

        if (home_address_form.is_valid() and
            contact_address_form.is_valid()):
            home_address = home_address_form.save()
            contact_address = contact_address_form.save()

            applicant_address = ApplicantAddress(
                applicant=applicant,
                home_address=home_address,
                contact_address=contact_address)

            if have_old_address:
                applicant_address.id = old_applicant_address.id

            applicant_address.save()
            applicant.add_related_model('address',
                                        save=True,
                                        smart=True)

            return (True, home_address_form, contact_address_form)
    else:
        home_address_form = AddressForm(prefix="home",
                                        instance=old_home_address)
        contact_address_form = AddressForm(prefix="contact",
                                           instance=old_contact_address)

    return (False, home_address_form, contact_address_form)

