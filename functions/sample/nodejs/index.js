/**
 * Get all databases
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

    try {
        let dbList = await cloudant.db.list();
        return { "dbs": dbList };
    } catch (error) {
        return { error: error.description };
    }
}

//  const { CloudantV1 } = require("@ibm-cloud/cloudant");
//  const { IamAuthenticator } = require("ibm-cloud-sdk-core");
 
//  function main(params) {
//    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
//    const cloudant = CloudantV1.newInstance({
//      authenticator: authenticator,
//    });
//    cloudant.setServiceUrl(params.COUCH_URL);
 
//    let dbList = getDbs(cloudant);
//    return { dbs: dbList };
//  }
 
//  function getDbs(cloudant) {
//    cloudant
//      .getAllDbs()
//      .then((body) => {
//        body.forEach((db) => {
//          dbList.push(db);
//        });
//      })
//      .catch((err) => {
//        console.log(err);
//      });
//  }