import { useEffect, useState } from "react";
import { BsArrowCounterclockwise, BsCreditCardFill } from "react-icons/bs";
import { FaEdit, FaTrashAlt } from "react-icons/fa";
import { useNavigate } from "react-router";
import { Link } from "react-router-dom";
import useHeaders from "../../../app/header";
import { useAppDispatch, useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";
import Paginate from "../../products/Paginate";
import SearchBar from "../../products/Searchbar";
import { yaLog } from "../../slices/logIn";
import {
  categorias,
  deleteProd,
  fetchAllProducts,
  filter,
  orderByDisponible,
  orderByName,
  orderByPrice,
  orderByStock,
} from "../../slices/productSlice";

const PanelProductos = () => {
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [productsPerPage] = useState(9);
  const lastPostIndex = currentPage * productsPerPage;
  const firstPostIndex = lastPostIndex - productsPerPage;
  const dispatch = useAppDispatch();
  const data = useAppSelector((state: RootState) => state.products);
  const cate = useAppSelector((state) => state.products.categorias);
  const token = JSON.parse(window.localStorage.getItem("token") || "{}");
  const user = JSON.parse(window.localStorage.getItem("user") || "{}");
  const [orderSelect, setOrderSelect] = useState(true);
  const [cateSelect, setCateSelect] = useState(true);
  const navigate = useNavigate();
  const header = useHeaders(token);
  const [active, setActive] = useState(0);

  //============use effect=================

  useEffect(() => {
    dispatch(fetchAllProducts(""));
    dispatch(categorias());
    if (Object.keys(user).length) {
      dispatch(yaLog(user.email));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  //===========pagination=============
  const currentProducts = data.allProducts?.slice(
    firstPostIndex,
    lastPostIndex
  );
  const [pageLimit] = useState(5);
  const [maxPageNumberLimit, setMaxPageNumberLimit] = useState(5);
  const [minPageNumberLimit, setMinPageNumberLimit] = useState(0);

  //=====================click handlers=====================
  const handleCateFilter = (event: any) => {
    setCateSelect(false);
    if (event.target.value.length) {
      if (event.target.value === "all") {
        dispatch(fetchAllProducts(""));
      } else {
        dispatch(filter(event.target.value));
        setCurrentPage(1);
        setActive(0);
      }
    }
    setOrderSelect(true);
  };

  const handleRestore = (e: any) => {
    setOrderSelect(true);
    setCateSelect(true);
    dispatch(fetchAllProducts(""));
    setCurrentPage(1);
    setActive(0);
  };

  const handleOrder = (e: any) => {
    setOrderSelect(false);
    setCurrentPage(1);
    setActive(0);
    if (e.target.value === "alfa") {
      dispatch(orderByName("name-asc"));
    } else if (e.target.value === "stock") {
      dispatch(orderByStock());
    } else if (e.target.value === "disponible") {
      dispatch(orderByDisponible());
    } else if (e.target.value === "precio") {
      dispatch(orderByPrice("caro"));
    }
  };

  const handleDelProd = (e: any, id: string) => {
    dispatch(deleteProd(header.headers, id));
  };

  //==============render================================
  if (data?.allProducts instanceof Array) {
    return (
      <div className=" bg-white bg-admin-banner bg-no-repeat bg-contain h-full">
        <h1 className="text-white justify-center py-20 mb-2 text-5xl font-bold flex align-middle items-center">
          PANEL DE PRODUCTOS
        </h1>
        <div className=" mx-8 bg-white border-2 px-4 border-black rounded-lg">
          <div>
            <div className="grid grid-cols-[1.5fr_1fr] gap-8">
              <div className="grid grid-cols-[2fr_1fr_1fr_.2fr] gap-16  my-8">
                <SearchBar
                  setCurrentPage={setCurrentPage}
                  setActive={setActive}
                />
                <select
                  name="ordenar"
                  id="ordenar"
                  className="border border-black rounded-lg px-1"
                  onChange={(e) => handleOrder(e)}
                >
                  <option
                    value="placeholder"
                    disabled
                    hidden
                    selected={orderSelect}
                  >
                    Order by
                  </option>
                  <option value="alfa">Alfabetico</option>
                  <option value="stock">Stock</option>
                  <option value="disponible">Disponible</option>
                  <option value="precio">Precio</option>
                </select>
                <select
                  name="categorias"
                  id="categorias"
                  className="border border-black rounded-lg px-1 py-3"
                  onChange={(e) => handleCateFilter(e)}
                >
                  <option
                    value="placeholder"
                    disabled
                    hidden
                    selected={cateSelect}
                  >
                    Categorias
                  </option>
                  <option value="all">All</option>;
                  {cate?.map((cate: { name: string; _id: string }) => {
                    return <option value={cate.name}>{cate.name}</option>;
                  })}
                </select>
                <BsArrowCounterclockwise
                  onClick={(e) => handleRestore(e)}
                  size={30}
                  title="restaurar productos"
                  className="cursor-pointer"
                />
              </div>

              <div className=" self-center justify-self-center ">
                <button
                  onClick={() => navigate("/admin/products/crear-categoria")}
                  className="bg-[#855C20] mr-4 py-2 px-2 text-white rounded-lg font-semibold"
                >
                  CATEGORIA
                </button>
                <button
                  onClick={() => navigate("/admin/products/crear-producto")}
                  className="bg-[#855C20] py-2 px-2 text-white rounded-lg font-semibold"
                >
                  CREAR PRODUCTO
                </button>
              </div>
            </div>
            <div className="relative">
              <div className=" grid grid-cols-[1fr_.2fr_.2fr_.2fr] w-[55%] pr-8 gap-16 justify-items-center">
                <p>Nombre</p>
                <p>Stock</p>
                <p>Disponible</p>
                <p>Precio</p>
              </div>

              {currentProducts?.map((data) => {
                const disp = data.available ? "Sí" : "Nó";
                return (
                  <div
                    className="grid grid-cols-[1fr_.2fr_.2fr_1fr_.2fr_.2fr_.2fr]  gap-16 py-2 pl-2 mt-8 border border-black rounded-lg items-center"
                    key={data._id}
                  >
                    <p>{data.name}</p>
                    <p>{data.stock}</p>
                    <p>{disp}</p>
                    <p>{data.price}</p>
                    <Link
                      className="w-4"
                      to={`/admin/products/hisrotial-producto/${data._id}`}
                    >
                      <BsCreditCardFill
                        className="w-4 cursor-pointer "
                        title="ver historial de compra de producto"
                      />
                    </Link>
                    <Link className="w-4" to={`editar-producto/${data._id}`}>
                      <FaEdit
                        className="w-4 cursor-pointer "
                        title="Editar producto"
                      />
                    </Link>
                    <FaTrashAlt
                      className="justify-self-center cursor-pointer "
                      title="Eliminar producto"
                      onClick={(e) => {
                        handleDelProd(e, data._id);
                      }}
                    />
                  </div>
                );
              })}
            </div>
            <Paginate
              allProducts={data.allProducts.length}
              productsPerPage={productsPerPage}
              setCurrentPage={setCurrentPage}
              currentPage={currentPage}
              pageLimit={pageLimit}
              maxPageNumberLimit={maxPageNumberLimit}
              minPageNumberLimit={minPageNumberLimit}
              setMaxPageNumberLimit={setMaxPageNumberLimit}
              setMinPageNumberLimit={setMinPageNumberLimit}
              active={active}
              setActive={setActive}
            />
          </div>
        </div>
      </div>
    );
  } else {
    return <div>Error</div>;
  }
};

export default PanelProductos;
