const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    
    let reviewPromise = postReview(cloudant, 'reviews', params.review);
    return reviewPromise;
}

function postReview(cloudant, dbname, review) {
    let doc = review;

    return new Promise((resolve, reject) => {
        cloudant.postDocument({ db:dbname, document: doc })
            .then((result) => {
                if (result.result.ok) {
                    cloudant.getDocument({ db:dbname, docId: result.result.id})
                        .then((res) => {
                            let review = res.result;
                            delete review._id;
                            delete review._rev;
                            resolve({review: review});
                        })
                        .catch(err => {
                            reject({ err: err.message });
                        });
                    
                }
            })
            .catch(err => {
                console.log(err);
                reject({ err: err.message });
            });
    });
}
