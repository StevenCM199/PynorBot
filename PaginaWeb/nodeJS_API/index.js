const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const http = require('http')
const fs = require('fs')

const app = express();

app.use(cors());
app.use(bodyParser.json());

const Pool = require("pg").Pool;
const pool = new Pool({
  user: "jrwiqonwasncwd",
  host: "ec2-54-157-16-196.compute-1.amazonaws.com",
  database: "ddfvf61h5p68j5",
  password: "498dbceebaae97327b74e9a8ada19c7e08b0436d47fdb2dac37eef0aee71c753",
  port: 5432,
  ssl: {    /* <----- Add SSL option */
  rejectUnauthorized: false,},
});

app.get("/api/v1/ezGet", (req, res) => {
    pool.query(
      "SELECT * from times_test",
      [],
      (error, results) => {
        if (error) {
          throw error;
        }
  
        res.status(200).json(results.rows);
      }
    );
  });


app.post("/api/v1/ezInsert", (req, res) => {
    const { discordID, hours, lastTimeConnected } = req.body;
  
    pool.query(
      "INSERT INTO times_test (discordID, hours, lastTimeConnected) VALUES ($1, $2, $3)",
      [discordID, hours, lastTimeConnected],
      (error, results) => {
        if (error) {
          throw error;
        }
  
        res.sendStatus(201);
      }
    );
  });

  http
  .createServer((request, response) => {
      fs.readFile(`.${request.url}`, (err, data) => {
          if (err) {
              response.writeHeader(404, {
                  'Content-Type': 'text/plain'
              })
              response.write('404 Not Found')
              response.end()
              return
          }

          if (request.url.endsWith('.html')) {
              response.writeHeader(200, {
                  'Content-Type': 'text/html'
              })
          }

          if (request.url.endsWith('.js')) {
              response.writeHeader(200, {
                  'Content-Type': 'application/javascript'
              })
          }

          response.write(data)
          response.end()
      })
  }) 


app.listen(8000, () => {
  console.log(`Server is running.`);
});