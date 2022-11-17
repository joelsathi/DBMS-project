const http = require("http");

const hostname = "127.0.0.1";
const port = 3000;

const server = http.createServer((req, res) => {
  var url = req.url;
  switch (url) {
    case "/":
      res.statusCode = 200;
      res.setHeader("Content-Type", "text/html");
      res.write("<h1>Welcome to Thulasi Stores</h1>");
      res.end();
      break;

    case "/about":
      res.statusCode = 200;
      res.setHeader("Content-Type", "text/html");
      res.write(
        "This is the project thulasi stores which we are doing for dbms"
      );
      res.end("");
      break;

    default:
      res.statusCode = 404;
      res.setHeader("Content-Type", "text/html");
      res.write("Page Not Found");
      res.end();
      break;
  }
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
