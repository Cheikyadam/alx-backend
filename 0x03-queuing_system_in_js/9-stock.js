import express from 'express';
import { createClient, print } from 'redis';
const { promisify } = require('util');

const listProducts = [
  {'Id': 1, 'name': 'Suitcase 250', 'price': 50, 'stock': 4},
  {'Id': 2, 'name': 'Suitcase 450', 'price': 100, 'stock': 10},
  {'Id': 3, 'name': 'Suitcase 650', 'price': 350, 'stock': 2},
  {'Id': 4, 'name': 'Suitcase 1050', 'price': 550, 'stock': 5}
];

function getItemById(id){
 for (const prod of listProducts){
   if (prod.Id == id){
     return prod;
   }
 }
}

const  client = createClient();
client.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`));
client.on('connect', () => console.log('Redis client connected to the server'));


function reserveStockById(itemId, stock){
  client.set(itemId, stock.toString());  
}

const getAsync = promisify(client.get).bind(client);

async function getCurrentReservedStockById(itemId){
  try{
    const reply = await getAsync(itemId);
    return reply;
  }
  catch (err) {
    console.log(`Error: ${err.message}`);
  } 
}

const app = express();

app.use(express.json());

app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const prod = getItemById(itemId);
  if (prod === undefined){
    res.statusCode = 404;
    res.json({"status": "Product not found"});
  }
  else {
    let stock = prod.stock;
    try {
    stock = await getCurrentReservedStockById(itemId);
    console.log(`stock: ${stock}`);
    }
    catch (err) {}
    if (stock === null){
      stock = prod.stock;
    }
   res.json({"itemId":prod.Id, "itemName": prod.name, "price": prod.price, "initialAvailableQuantity": prod.stock, "currentQuantity": stock}); 
  }
});


app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const prod = getItemById(itemId);
  if (prod === undefined){
    res.statusCode = 404;
    res.json({"status": "Product not found"});
  }
  else {
    let stock = prod.stock;
    try {
    stock = await getCurrentReservedStockById(itemId);
    console.log(`stock: ${stock}`);
    }
    catch (err) {}
    if (stock === null){
      stock = prod.stock;
    }
    if (stock <= 0){
      res.json({"status":"Not enough stock available","itemId":itemId});
    } else{
      reserveStockById(itemId, stock - 1);
      res.json({"status":"Reservation confirmed","itemId":itemId});
    }
  }
});

app.get('/list_products', (req, res) => {
  let prods = [];
  for (const prod of listProducts){
    const cur = {"itemId":prod.Id, "itemName": prod.name, "price": prod.price, "initialAvailableQuantity": prod.stock};
    prods.push(cur);
  }
  res.json(prods);
});


app.listen(1245, () => {
  console.log('app running in port 1245');
});



