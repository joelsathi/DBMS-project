import * as React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
// Personal Information
function createData(
    username: string,
    firstname: string,
    lastname: string,
    email: string,
    address: string,
    mobile_no: string,
  ) {
    return { username, firstname, lastname, email, address, mobile_no };
  }
  
  const info =
    createData(
        'thulasithang',
        'Thulasithan',
        'Gnanenthiram',
        'thulasithang@sample.com',
        'T56: Bayawechcha paara, anda yata',
        '0112729729', 
    );


export default function PersonalInfo() {
  return (
    <React.Fragment>
    <Card sx={{ minWidth: 275, boxShadow: 4, borderRadius: '16px'}}>
      <CardContent>
      <Typography
                    variant="h5"
                    color="inherit"
                  >
                  {info.firstname} {info.lastname}
            </Typography>
            <Typography
                    variant="body1"
                    color="inherit"
                  >
                @{info.username}
            </Typography>
            <Typography
                    variant="body1"
                    color="inherit"
                  >
                {info.email}
            </Typography>
            <Typography
                    variant="body1"
                    color="inherit"
                  >
                {info.address}
            </Typography>
            <Typography
                    variant="body1"
                    color="inherit"
                  >
                {info.mobile_no}
            </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" variant='outlined' color="inherit" sx={{ marginLeft: "auto" }}>Edit info</Button>
      </CardActions>
    </Card>
    </React.Fragment>
    );
}