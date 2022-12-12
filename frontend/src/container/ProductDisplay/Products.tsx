import { Grid } from '@mui/material';
import * as React from 'react';
import { forEachChild } from 'typescript';
import ProductCard from './ProductCard';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// Generate Order Data
function createData(
  productId: number,
  productName: string,
  productPrice: number,
  productImageUrl: string,
) {
  return { productName, productPrice, productImageUrl };
}
const products = [
  createData(
    0,
    'iPhone 14 Pro',
    1000000.00,
    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-card-40-iphone14pro-202209?wid=340&hei=264&fmt=p-jpg&qlt=95&.v=1663611329492',
  ),
  createData(
    1,
    'iPhone 15 Pro',
    1000000.00,
    'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-card-40-iphone14pro-202209?wid=340&hei=264&fmt=p-jpg&qlt=95&.v=1663611329492',
  ),
  // createData(
  //   2,
  //   'iPhone 16 Pro',
  //   1000000.00,
  //   'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-card-40-iphone14pro-202209?wid=340&hei=264&fmt=p-jpg&qlt=95&.v=1663611329492',
  // ),
  // createData(
  //   3,
  //   'iPhone 17 Pro',
  //   1000000.00,
  //   'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-card-40-iphone14pro-202209?wid=340&hei=264&fmt=p-jpg&qlt=95&.v=1663611329492',
  // ),
  // createData(
  //   4,
  //   'iPhone 18 Pro',
  //   1000000.00,
  //   'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-card-40-iphone14pro-202209?wid=340&hei=264&fmt=p-jpg&qlt=95&.v=1663611329492',
  // ),
  // createData(
  //   5,
  //   'iPhone 20 Pro',
  //   1000000.00,
  //   'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-card-40-iphone14pro-202209?wid=340&hei=264&fmt=p-jpg&qlt=95&.v=1663611329492',
  // ),
];

export default function Products() {
  return (
    <React.Fragment>

    // iterate through the products array and pass the product data to the ProductCard component

      {products.map((product) => (
            <ProductCard productName={product.productName} productPrice={product.productPrice} productImageUrl={product.productImageUrl} />
          ))}
    </React.Fragment>
  );
}

// export default function Products() {
//   return (    
//       <Card sx={{ maxWidth: 345 }}>
//       <CardContent>
//         <Typography gutterBottom variant="h5" component="div">
//           {products[0].productName}
//         </Typography>
//         <CardMedia
//           component="img"
//           alt="iphone"
//           height="auto"
//           image={products[0].productImageUrl} />
//       </CardContent>
//       <Box sx={{ display: 'flex', alignItems: 'center', pl: 1, pb: 1 }}>
//         <Grid item xs={8}>
//           <Typography variant="body1" color="inherit" component="div">
//             Rs.{products[0].productPrice}
//           </Typography>
//         </Grid>
//         <Grid item xs={4}>
//           <CardActions>
//             <Button size="small" variant='outlined' color="inherit" sx={{ marginLeft: "-60" }}>Buy</Button>
//           </CardActions>
//         </Grid>
//       </Box>
//     </Card>
//   );
// }