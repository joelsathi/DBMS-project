import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { Grid } from '@mui/material';

export default function ProductCard(productName: string, productPrice: number, productImageUrl: string) {
    return (
        <Card sx={{ maxWidth: 345 }}>
            <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                    {productName}
                </Typography>
                <CardMedia
                    component="img"
                    alt="iphone"
                    height="auto"
                    image={productImageUrl} />
            </CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', pl: 1, pb: 1 }}>
                <Grid item xs={8}>
                    <Typography variant="body1" color="inherit" component="div">
                        Rs. {productPrice}
                    </Typography>
                </Grid>
                <Grid item xs={4}>
                    <CardActions>
                        <Button size="small" variant='outlined' color="inherit" sx={{ marginLeft: "-60" }}>Buy</Button>
                    </CardActions>
                </Grid>
            </Box>
        </Card>
    );
}