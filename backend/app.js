
const express = require("express")
const app = express()
const host = "localhost"
const port = 3001

const router = express.Router()
router.get("/", (req, res) => {
  res.send("Hello World")
})
router.get("/about", (req, res) => {
  res.json({projectName: "Thulasi", description: "Some Description"})
})
app.use(router)

app.listen(port, host, () => {
  console.log(`Server running on port ${port}`)
})