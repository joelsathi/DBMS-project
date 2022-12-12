import { Admin, Resource, ListGuesser, CustomRoutes } from "react-admin";
import jsonServerProvider from "ra-data-json-server";
import { UserDashboard } from "./container/UserDashboard";
import { ProductDisplay } from "./container/ProductDisplay";
// import { index } from "./container";
import { Route } from "react-router-dom";

const dataProvider = jsonServerProvider("https://jsonplaceholder.typicode.com");

const App = () => (
  <Admin dataProvider={dataProvider}>
    {/* <UserDashboard name="akw" /> */}
    {/* <Resource name="Dashboard" /> */}
    {/* <Dashboard /> */}
    {/* <Resource name="posts" list={ListGuesser} /> */}
    {/* <Resource name="comments" list={ListGuesser} /> */}
    <CustomRoutes> 
      <Route path="/ProductDisplay" element={<ProductDisplay/>}/>
    </CustomRoutes>
  </Admin>
  // <div>
  //   {/* <UserDashboard /> */}
  //   <ProductDisplay/>
  // </div>
);

export default App;
