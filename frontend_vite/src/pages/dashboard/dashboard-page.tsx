import { useEffect } from 'react';
import { Row, Col, Card } from 'react-bootstrap';
import DashboardLayout from '../../components/layouts/dashboard-layout';
import { useAppDispatch, useAppSelector } from '../../redux';
import { getOrdersList } from '../../redux/orders/slice-list';
import { formatCurrency } from '../../utils/helper';

const DashboardPage = () => {
  const { total } = useAppSelector((state) => state.productFilter);
  const { orders } = useAppSelector((state) => state.orders);
  const { users } = useAppSelector((state) => state.userList);
  const dispatch = useAppDispatch();

  const getTotalCost = () => {
    let total = 0;
    if (!orders) return 500.3;
    orders.map((item: any) => {
      if (!item) return;
      total += item.totalPrice;
    });
    return total;
  };

  // const totalPrice = getTotalCost();

  useEffect(() => {
    dispatch(getOrdersList());
  }, [dispatch]);

  return (
    <DashboardLayout>
      <Row className='g-6 my-6'>
        <Col md={4}>
          <Card className=' shadow border-0'>
            <Card.Body>
              <Row>
                <Col>
                  <span className='h3 font-bold mb-0'>
                    Welcome to the admin dashboard
                  </span>
                  <span className='h3 font-bold mb-0'>
                    {/* {formatCurrency(totalPrice)} */}
                  </span>
                </Col>
                <div className='col-auto'>
                  <div className='icon icon-shape bg-tertiary text-white text-lg rounded-circle'>
                    <i className='bi bi-credit-card' />
                  </div>
                </div>
              </Row>
              {/* <div className='mt-2 mb-0 text-sm'>
                <span className='badge badge-pill bg-soft-success text-success me-2'>
                  <i className='bi bi-arrow-up me-1' />
                  13%
                </span>
                <span className='text-nowrap text-xs text-muted'>
                since the last month
                </span>
              </div> */}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </DashboardLayout>
  );
};

export default DashboardPage;
