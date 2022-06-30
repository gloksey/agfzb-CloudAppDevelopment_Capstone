const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    
    let reviewPromise = getReviewByDealership(cloudant, 'reviews', params.dealerId);
    return reviewPromise;
}

function getReviewByDealership(cloudant, dbname, dealerId) {
    let selector = {dealership: {'$eq': parseInt(dealerId)}};
    let fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year'];
    return new Promise((resolve, reject) => {
        cloudant.postFind({ db:dbname, selector:selector, fields:fields })
            .then((result) => {
                if (result.result.docs.length > 0) {
                    resolve({result: result.result.docs});
                }
                else {
                    throw new Error('404: dealerId does not exist'); 
                }
            })
            .catch(err => {
                console.log(err);
                reject({ err: err.message });
            });
    });
}

function getAllDealerships(cloudant, dbname) {
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({ db: dbname, includeDocs: true })
            .then((result) => {
                if (result.result.total_rows > 0) {
                    let dealerships = [];
                    result.result.rows.forEach(row => {
                        dealerships.push({
                            'id': row.doc.id,
                            'city': row.doc.city,
                            'state': row.doc.state,
                            'st': row.doc.st,
                            'address': row.doc.address,
                            'zip': row.doc.zip,
                            'lat': row.doc.lat,
                            'long': row.doc.long
                        });
                    });
                    resolve({result: dealerships});
                }
                else {
                    throw new Error('404: The database is empty');
                }
            })
            .catch(err => {
                console.log(err);
                reject({ err: err.message });
            });
    });
}
