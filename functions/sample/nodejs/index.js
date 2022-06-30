const express = require('express');
const app = new express();

require('dotenv').config();

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const authenticator = new IamAuthenticator({ apikey: process.env.IAM_API_KEY })
const cloudant = CloudantV1.newInstance({
    authenticator: authenticator
});
cloudant.setServiceUrl(process.env.COUCH_URL);

app.get('/api/dealership', (req, res) => {
    let byState = req.query.state;
    if (byState !== undefined) {
        cloudant.postFind({ db: 'dealerships', selector: {st: {'$eq': byState}}, fields: ['id', 'city', 'state', 'st', 'address', 'zip', 'lat', 'long'] })
            .then(result => {
                if (result.result.docs.length > 0) {
                    return res.type('application/json').send(result.result.docs);
                }
                else {
                    return res.status(404).send(result);
                }
            })
            .catch(err => {
                return res.status(500).send('Something went wrong on the server:' + err);
            });
    }
    else {
        cloudant.postAllDocs({ db: 'dealerships', includeDocs: true })
            .then(result => {
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
                    return res.type('application/json').send(dealerships);
                }
                else {
                    return res.status(404).send('The database is empty');
                }
            })
            .catch(err => {
                return res.status(500).send('Something went wrong on the server:' + err);
            });
    }
});

let server = app.listen(8081, () => {
    console.log('Listening', server.address().port)
})
