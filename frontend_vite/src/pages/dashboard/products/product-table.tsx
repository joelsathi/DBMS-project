import { useEffect, useState } from 'react';
import { Button, Image, Row } from 'react-bootstrap';
import toast from 'react-hot-toast';
import { FaEdit, FaTrash } from 'react-icons/fa';
import { Link, useParams } from 'react-router-dom';
import DashboardLayout from '../../../components/layouts/dashboard-layout';
import ProductModal from '../../../components/modals/product-modal';
import Loader from '../../../components/UI/loader';
import Paginate from '../../../components/UI/paginate';
import TableContainer from '../../../components/UI/table-contrainer';
import { useAppDispatch, useAppSelector } from '../../../redux';
import { getFilterProducts } from '../../../redux/products/search-list';
import { getFilterProducts2 } from '../../../redux/products/rep1';
import authAxios from '../../../utils/auth-axios';
import { setError } from '../../../utils/error';
import { formatCurrency, getDate } from '../../../utils/helper';

// Then, use it in a component.
function ProductTable() {
  const dispatch = useAppDispatch();
  const { products, page, pages, loading } = useAppSelector(
    (state) => state.productFilter
  );
  const [refresh, setRefresh] = useState<boolean>(false);
  const [show, setShow] = useState<boolean>(false);
  const params = useParams();
  const pageNumber = params.pageNumber || 1;

  const onOpen = () => setShow(true);
  const onClose = () => setShow(false);

  const cols = [
    // 'image',
    // 'name',
    // 'brand',
    // 'category',
    // 'price',
    // 'created At',
    // 'options',
    "id",
    "sku",
    "year",
    "firstQuaterQty",
    "firstQuaterSales",
    "secondQuaterQty",  
    "secondQuaterSales",
    "thirdQuaterQty",
    "thirdQuaterSales",
    "fourthQuaterQty",
    "fourthQuaterSales",
    "total",  
  ];

  const onDelete = (id: string | number) => {
    if (window.confirm('are you sure?')) {
      authAxios
        .delete(`/products/${id}`)
        .then((res) => {
          toast.success('Product has beend deleted');
          setRefresh((prev) => (prev = !prev));
        })
        .catch((e) => toast.error(setError(e)));
    }
  };

  useEffect(() => {
    // dispatch(getFilterProducts({ n: pageNumber, b: '', c: '', q: '' }));
    dispatch(getFilterProducts2({ n: pageNumber, b: '', c: '', q: '' }));

  }, [dispatch, pageNumber, refresh]);

  return (
    <DashboardLayout>
      {loading ? (
        <Loader />
      ) : (
        <Row className='py-3'>
          <h3 className='d-flex justify-content-between align-items-center'>
            <span>Quartely sales report</span>
            {/* <Button
              style={{ backgroundColor: '#e03a3c', color: '#fff' }}
              variant='outline-none'
              onClick={onOpen}
              size='sm'
            >
              Add Product
            </Button> */}
          </h3>
          <TableContainer cols={cols}>
            {products.map((product) => (
              <tr key={product.sku}>
                <td>{product.id}</td>
                <td>{product.sku}</td>
                <td>{product.year}</td>
                <td>{product.firstQuaterQty}</td>
                <td>{formatCurrency(product.firstQuaterSales)}</td>
                <td>{product.secondQuaterQty}</td>
                <td>{formatCurrency(product.secondQuaterSales)}</td>
                <td>{product.thirdQuaterQty}</td>
                <td>{formatCurrency(product.thirdQuaterSales)}</td>
                <td>{product.fourthQuaterQty}</td>
                <td>{formatCurrency(product.fourthQuaterSales)}</td>
                <td>{product.total}</td>
              </tr>
            ))}
          </TableContainer>
        </Row>
      )}
      <Paginate pages={pages} page={page} isAdmin={true} keyword={''} />
      <ProductModal setRefresh={setRefresh} show={show} handleClose={onClose} />
    </DashboardLayout>
  );
}

export default ProductTable;
