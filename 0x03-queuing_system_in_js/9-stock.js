import express from "express";
import { defaults } from "request";
import redis from "redis";
import { promisify } from "node:util";

const redisClient = redis.createClient();
const redisGetAsync = promisify(redisClient.get).bind(redisClient);
const redisSetAsync = promisify(redisClient.set).bind(redisClient);

const listProducts = [
  {
    itemId: 1,
    itemName: "Suitcase 250",
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: "Suitcase 450",
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: "Suitcase 650",
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: "Suitcase 1050",
    price: 550,
    initialAvailableQuantity: 5,
  },
];

function getItemById(id) {
  return listProducts.find((item) => item.itemId === id);
}

async function reserveStockById(itemId, stock) {
  await redisSetAsync(itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
  return await redisGetAsync(itemId);
}

const app = express();

const port = 1245;
const hostname = "localhost";

app.get("/list_products", (req, res) => {
  res.json(listProducts);
});

app.get("/list_products/:itemId", async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    res.status(404).json({ status: "Product not found" });
  } else {
    item.currentQuantity = await getCurrentReservedStockById(itemId);
    if (item.currentQuantity === null) {
      item.currentQuantity = item.initialAvailableQuantity;
      await reserveStockById(itemId, item.initialAvailableQuantity);
    }
    res.json(item);
  }
});

app.get("/reserve_product/:itemId", async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);

  if (item === undefined) {
    res.json({ status: "Product not found" });
  } else {
    const currentQuantity = parseInt(await getCurrentReservedStockById(itemId));
    if (currentQuantity === undefined) {
      await reserveStockById(itemId, item.initialAvailableQuantity - 1);
      console.log("hi");
    } else if (currentQuantity === 0) {
      res.json({ status: "Not enough stock available", itemId: itemId });
    } else {
      await reserveStockById(itemId, currentQuantity - 1);
      res.json({ status: "Reservation confirmed", itemId: itemId });
    }
  }
});

app.listen(port, hostname);

export default app;
