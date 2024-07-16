const fs = require('node:fs');

async function getData(url = '') {
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit'
    });
    return response.json();
  }

function randomCat() {
    const i = Math.floor(Math.random() * 3)
    const cats = ['Primary', 'Component', 'Processed']
    return cats[i];

}
async function data() {
    let data = await getData('https://entity.api.sennetconsortium.org/datasets/sankey_data')

    for (let item of data) {
        item['data_category'] = randomCat()
    }

    fs.writeFile('./sankey.json', JSON.stringify(data), { flag: 'a+' }, err => {});
}

data()