import firebase_admin
from firebase_admin import credentials, initialize_app, storage, firestore
from io import BytesIO

class firebaseStore:
    def __init__(self):

        try:
            app = firebase_admin.get_app()
        except ValueError as e:
            cred = credentials.Certificate("assets/firebase_creds.json")
            firebase_admin.initialize_app(cred)

    # Create a new document in Firestore
    def create_document(self, document_data, collection = "history"):
        db = firestore.client()
        doc_ref = db.collection(collection).document()
        doc_ref.set(document_data)
        print('Document created with ID:', doc_ref.id)

    # Read a document from Firestore
    def read_all_document(self, collection = "history",):
        db = firestore.client()
        print(db)
        ## error here fix

        documents = db.collection(collection).get()
        print(documents)
        # Get all documents from the collection

        # Iterate over the documents
        docs = []
        for doc in documents:
            print(f"Document ID: {doc.id}")
            print(f"Document data: {doc.to_dict()}")
            docs += [doc.to_dict()]
        return docs
    
    # def store_firebase(self, response):
    #     bucket = storage.bucket('test-2e207.appspot.com')
    #     blob = bucket.blob(x['headline'])
    #     blob.upload_from_string(response, content_type='image/jpeg')
    #     blob.make_public()
    #     print("roli", blob.public_url)
store = firebaseStore()

def get_fr_store():
    return store