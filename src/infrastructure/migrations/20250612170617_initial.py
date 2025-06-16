from beanie import free_fall_migration

from infrastructure.models.notifications import NotificationTemplateModel


class Forward:
    @free_fall_migration(document_models=[NotificationTemplateModel])
    async def populate_notification_templates(self, session):
        templates = [
            NotificationTemplateModel(
                name='registration_successful',
                text_template='Dear %(first_name)s %(last_name)s %(middle_name)s we glad to inform you that your registration was successful!',
                html_template='Dear <strong>%(first_name)s %(last_name)s %(middle_name)s</strong> we glad to inform you that your registration was successful!'
            ),
            NotificationTemplateModel(
                name='registration_failed',
                text_template='Dear %(first_name)s %(last_name)s %(middle_name)s we sorry to inform you that your registration was not successful!',
                html_template='Dear <strong>%(first_name)s %(last_name)s %(middle_name)s</strong> we sorry to inform you that your registration was not successful!'
            ),
            NotificationTemplateModel(
                name='registration_pending',
                text_template='Dear %(first_name)s %(last_name)s %(middle_name)s we inform you that your registration is pending.',
                html_template='Dear <strong>%(first_name)s %(last_name)s %(middle_name)s</strong> we inform you that your registration is pending.'
            ),
            NotificationTemplateModel(
                name='email_update_initiated',
                text_template='Dear user, your email update has been initiated. Please follow the this link (http://localhost:8001/api/v1/me/credentials/email/verify?token=%(verify_token)s) to complete the process.',
                html_template='Dear <strong>user</strong>, your email update has been initiated. Please follow the this <a href="http://localhost:8001/api/v1/me/credentials/email/verify?token=%(verify_token)s">link</a> to complete the process.'
            ),
            NotificationTemplateModel(
                name='email_updated',
                text_template='Dear user, your email was successfully updated to %(new_email)s.',
                html_template='Dear <strong>user</strong>, your email was successfully updated to <strong>%(new_email)s</strong>.'
            ),
            NotificationTemplateModel(
                name='phone_number_update_initiated',
                text_template='Dear user, your phone number update has been initiated. Please follow the this link (http://localhost:8001/api/v1/me/credentials/phone-number/verify?token=%(verify_token)s) to complete the process.',
                html_template=None
            ),
            NotificationTemplateModel(
                name='phone_number_updated',
                text_template='Dear user, your phone number was successfully updated to %(new_phone_number)s.',
                html_template=None
            ),
            NotificationTemplateModel(
                name='password_reset_initiated',
                text_template='Dear user, your password reset has been initiated. Please follow the this link (http://localhost:8001/api/v1/password/reset?token=%(verify_token)s) to complete the process.',
                html_template='Dear <strong>user</strong>, your password reset has been initiated. Please follow the this <a href="http://localhost:8001/api/v1/password/reset?token=%(verify_token)s">link</a> to complete the process.'
            ),
        ]

        await NotificationTemplateModel.insert_many(documents=templates)


class Backward:
    @free_fall_migration(document_models=[NotificationTemplateModel])
    async def remove_notification_templates(self, session):
        await NotificationTemplateModel.delete_all()
