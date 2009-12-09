from application.models import Applicant, SubmissionInfo

def get_submitted_applicant_dict(join_fields=None):
    app_dict = {}
    for app in Applicant.objects.all():
        app_dict[app.id] = app

    field_data = {}

    for field, field_class in join_fields.iteritems():
        data = {}
        for obj in field_class.objects.all():
            data[obj.applicant_id] = obj
        field_data[field] = data

    applicants = {}
    for submission_info in SubmissionInfo.objects.all():
        app_id = submission_info.applicant_id

        applicant = app_dict[app_id]
        applicant.submission_info = submission_info

        for field in join_fields.iterkeys():
            if app_id in field_data[field]:
                applicant.__setattr__(field, field_data[field][app_id])

        applicants[app_id] = applicant

    return applicants
