from google.oauth2 import service_account
import googleapiclient.discovery

SCOPES = ['https://www.googleapis.com/auth/admin.directory.device.mobile']
SERVICE_ACCOUNT_FILE = 'auth.json'
EMAIL_ACCOUNT = '<INSERTTHEEMAILADDRESSHERE>'


def get_credential():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(EMAIL_ACCOUNT)
    # admin = googleapiclient.discovery.build('admin', 'directory_v1', credentials=credentials)
    admin = googleapiclient.discovery.build('admin', 'directory_v1', credentials=delegated_credentials)
    return admin


def get_mobiledevice_list(admin, customerId):
    results = admin.mobiledevices().list(customerId=customerId).execute()
    mobiledevices = results.get('mobiledevices', [])
    print('mobile devices name and resourceId')
    for mobiledevice in mobiledevices:
        print(u'{0} ({1})'.format(mobiledevice['name'], mobiledevice['resourceId']))
    return results


def action_mobiledevice(admin, customerId, resourceId, actionName):  # actionName: "approve", "block",etc
    body = dict(action=actionName)
    results = admin.mobiledevices().action(customerId=customerId, resourceId=resourceId, body=body).execute()
    return results


def main():
    admin = get_credential()
    customerId = '<INSERTTHECUSTOMERIDHERE>'
    resourceId = '<INSERTTHEJWTHERE>'
    action = "approve"
    #action = "block"

    mobiledevice_list = get_mobiledevice_list(admin, customerId)
    print(mobiledevice_list)

    action_mobiledevice(admin, customerId, resourceId, action)
    print ("Approved successfully")


if __name__ == '__main__':
    main()
