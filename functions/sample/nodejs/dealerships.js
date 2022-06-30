const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    
    let dealershipsPromise = 0;
    if (params.state !== undefined) {
        dealershipsPromise = getDealershipsByState(cloudant, 'dealerships', params.state);
    }
    else {
        dealershipsPromise = getAllDealerships(cloudant, 'dealerships');
    }
    return dealershipsPromise;
}

function getDealershipsByState(cloudant, dbname, byState) {
    let selector = {st: {'$eq': byState}};
    let fields = ['id', 'city', 'state', 'st', 'address', 'zip', 'lat', 'long'];
    return new Promise((resolve, reject) => {
        cloudant.postFind({ db:dbname, selector:selector, fields:fields })
            .then((result) => {
                if (result.result.docs.length > 0) {
                    resolve({result: result.result.docs});
                }
            })
            .catch(err => {
                console.log(err);
                reject({ err: err });
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
            })
            .catch(err => {
                console.log(err);
                reject({ err: err });
            });
    });
}
