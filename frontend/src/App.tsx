import { Admin, Resource, ListGuesser, CustomRoutes } from "react-admin";
import jsonServerProvider from "ra-data-json-server";
import { Route } from "react-router-dom";


import { Checkout, SingleProduct, Testing } from "./container";

// const addnums = (num1: number, num2: number) => { return num1 + num2}

const dataProvider = jsonServerProvider("https://jsonplaceholder.typicode.com");

const App = () => (
  // <SingleProduct />
  // <Admin dataProvider={dataProvider}>
  //   {/* <Resource name="posts" list={ListGuesser} />
  //   <Resource name="comments" list={ListGuesser} /> */}
  //   {/* <Route path="/Checkout" element={<SingleProduct/>}/> */}
    
  // </Admin>
  // <CustomRoutes>
  // {/* <Route path="/Checkout" element={<Checkout/>} /> */}
  //   <Route path="/Checkout" element={<SingleProduct/>} />
  // </CustomRoutes>
  <SingleProduct />
  // <Checkout />
  // <Testing />
);

export default App;
