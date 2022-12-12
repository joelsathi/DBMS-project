import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import { styled } from '@mui/material/styles';

// Generate Order Data
function createData(
  order_id: number,
  billing_date: string,
  items: string,
  shipTo: string,
  paymentMethod: string,
  amount: number,
) {
  return { order_id, billing_date, items, shipTo, paymentMethod, amount };
}
const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));
const rows = [
  createData(
    0,
    '2022-02-14',
    'Teddy bear',
    'T56: Bayawechcha paara, anda yata',
    'VISA ⠀•••• 3719',
    1000.00,
  ),
  createData(
    1,
    '2022-12-14',
    'Apple Iphone 12',
    'AK24: Bayawechcha paara, anda yata',
    'VISA ⠀•••• 3719',
    200000.00,
  ),
];


export default function Orders() {
  return (
    <React.Fragment>
      <Title>Recent Orders</Title>
      <Table size="medium">
        <TableHead>
          <StyledTableRow>
            <StyledTableCell>Billing Date</StyledTableCell>
            <StyledTableCell>Items</StyledTableCell>
            <StyledTableCell>Ship To</StyledTableCell>
            <StyledTableCell>Payment Method</StyledTableCell>
            <StyledTableCell align="right">Total Amount</StyledTableCell>
          </StyledTableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <StyledTableRow key={row.order_id}>
              <StyledTableCell>{row.billing_date}</StyledTableCell>
              <StyledTableCell>{row.items}</StyledTableCell>
              <StyledTableCell>{row.shipTo}</StyledTableCell>
              <StyledTableCell>{row.paymentMethod}</StyledTableCell>
              <StyledTableCell align="right">{`Rs.${row.amount}`}</StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}
