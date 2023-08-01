import { Express } from "express";
import express from "express";
import { Request, Response } from "express";
import { connect } from "mongoose";
import { route } from "./routes/routes";
import * as bodyParser from "body-parser";
import * as dotenv from "dotenv";
import cors from "cors";
import helmet from "helmet";

dotenv.config();

const url: string = process.env.MONGO_URI
  ? process.env.MONGO_URI
  : "URI";

connect(url);

const app: Express = express();
const port = 4000;

app.use(bodyParser.json())
app.use('/api', route);
app.use(cors());
app.use(helmet());

app.get("/", (req: Request, res: Response) => {
  res.send("<h1>Welcome to ExpressTs-App</h1>");
});

app.listen(port);
