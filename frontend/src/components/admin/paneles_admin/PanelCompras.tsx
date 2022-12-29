import { useEffect, useState } from "react";
import { BsArrowCounterclockwise } from "react-icons/bs";
import { Link } from "react-router-dom";
import useHeaders from "../../../app/header";
import { useAppDispatch, useAppSelector } from "../../../app/hooks";
import Paginate from "../../products/Paginate";
import {
  cambiarEstadoOrden,
  cambiarEstadoOrdenCancelada,
  cambiarEstadoOrdenCompleta,
  despacharOrden,
  filterOrderState,
  getAllOrders,
} from "../../slices/admin";
import { yaLog } from "../../slices/logIn";
import OrderSearch from "../OrderSearch";

const PanelCompras = () => {
  const token = JSON.parse(window.localStorage.getItem("token") || "{}");
  const user = JSON.parse(window.localStorage.getItem("user") || "{}");
  const header = useHeaders(token);
  const dispatch = useAppDispatch();
  const ordenes = useAppSelector((state) => state.admin.orders);
  const [searchBy, setSearchBy] = useState("");
  const [buscarSelect, setBuscarSelect] = useState(true);
  const [cateSelect, setCateSelect] = useState(true);

  useEffect(() => {
    dispatch(yaLog(user.email));
    dispatch(getAllOrders(header.headers));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  //=================pagination=======================//
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [productsPerPage] = useState(15);
  const [pageLimit] = useState(5);
  const [maxPageNumberLimit, setMaxPageNumberLimit] = useState(5);
  const [minPageNumberLimit, setMinPageNumberLimit] = useState(0);
  const lastPostIndex = currentPage * productsPerPage;
  const firstPostIndex = lastPostIndex - productsPerPage;
  const currentProducts = ordenes.length
    ? ordenes?.slice(firstPostIndex, lastPostIndex)
    : [];
  const [active, setActive] = useState(0);

  //===============handlers===========================//

  const handleRestore = () => {
    setBuscarSelect(true);
    setCateSelect(true);
    dispatch(getAllOrders(header.headers));
    setCurrentPage(1);
    setActive(0);
  };

  const handleEstado = (id: string, newState: string) => {
    if (newState === "Completa") {
      dispatch(cambiarEstadoOrdenCompleta(header.headers, id));
    } else if (newState === "Cancelada") {
      dispatch(cambiarEstadoOrdenCancelada(header.headers, id));
    } else {
      dispatch(cambiarEstadoOrden(header.headers, id, newState));
    }
  };

  const handlePerfil = (id: string) => {};

  const handleSearchBy = (e: any) => {
    setSearchBy(e.target.value);
  };

  const handleFilter = (e: any) => {
    dispatch(filterOrderState(e.target.value));
    setCurrentPage(1);
    setActive(0);
  };

  const handleDespachar = (id: string) => {
    dispatch(despacharOrden(header.headers, id));
    window.location.reload();
  };

  //==========================render================
  return (
    <div className="flex flex-col bg-white bg-bg-historial bg-no-repeat bg-contain ">
      <h1 className="text-white justify-center py-20 mb-2 text-5xl font-bold flex align-middle items-center">
        PANEL DE COMPRAS
      </h1>
      <div className=" mx-8 bg-white border-2 px-4 border-black rounded-lg">
        <div>
          <div className="flex  gap-8 mt-10">
            <OrderSearch
              searchBy={searchBy}
              setCurrentPage={setCurrentPage}
              setActive={setActive}
            />
            <select
              className="outline-none"
              onChange={(e) => handleSearchBy(e)}
            >
              <option
                value="placeholder"
                disabled
                hidden
                selected={buscarSelect}
              >
                Buscar por
              </option>
              <option value="name">Name</option>
              <option value="id">Id</option>
            </select>
            <select className="outline-none" onChange={(e) => handleFilter(e)}>
              <option value="placeholder" disabled hidden selected={cateSelect}>
                Filtrar por estado
              </option>
              <option value="Completa">Completa</option>
              <option value="Cancelada">Cancelada</option>
              <option value="Creada">Procesando</option>
              <option value="Enviada">Despachada</option>
            </select>
          </div>

          <div className="grid grid-cols-[1.5fr_1fr] gap-8"></div>
          <div className="mt-8">
            <div className=" grid grid-cols-[1fr_.5fr_.5fr_.5fr_1.5fr_.5fr] gap-16 ml-20">
              <p>Email</p>
              <p>Id de orden</p>
              <p>Precio total</p>
              <p>Estado</p>
              <p>Cambiar estado</p>
              <BsArrowCounterclockwise
                onClick={() => handleRestore()}
                size={30}
                title="restore products cursor-pointer"
                className="cursor-pointer"
              />
            </div>

            {currentProducts.map((data) => {
              const estilo =
                data.state === "Completa"
                  ? "text-lime-500"
                  : data.state === "Cancelada"
                  ? "text-red-600"
                  : "";

              const estado =
                data.state === "Completa"
                  ? "COMPLETA"
                  : data.state === "Cancelada"
                  ? "CANCELADA"
                  : data.state === "Enviada"
                  ? "DESPACHADA"
                  : "PROCENSANDO";

              const price = data.products?.reduce((prev, curr) => {
                return prev + curr.price;
              }, 0);
              return (
                <div
                  className="grid grid-cols-[1fr_1fr_.2fr_.4fr_2fr_1fr] gap-6 break-words py-2 pl-2 mt-8 border border-black rounded-lg items-center"
                  key={data._id}
                >
                  <p
                    onClick={() => {
                      handlePerfil(data._id);
                    }}
                  >
                    {data.user}
                  </p>
                  <p>{data._id}</p>
                  <p>{price.toFixed(2)}</p>
                  <p className={`text-sm ${estilo}`}>{estado}</p>
                  <div className="flex gap-4 ">
                    <button
                      onClick={() => handleEstado(data._id, "Completa")}
                      className="border-r border-black pr-4 hover:text-[#855C20] font-semibold "
                    >
                      Completa
                    </button>
                    <button
                      onClick={() => handleEstado(data._id, "Cancelada")}
                      className="border-r border-black pr-4 hover:text-[#855C20] font-semibold "
                    >
                      Cancelada
                    </button>
                    <button
                      onClick={() => handleEstado(data._id, "Creada")}
                      className=" pr-4 hover:text-[#855C20] font-semibold "
                    >
                      Procesando
                    </button>
                    {data.state === "Completa" && (
                      <button
                        onClick={() => handleDespachar(data._id)}
                        className="border border-black px-2 hover:bg-[#855C20] hover:text-white text-sm "
                      >
                        DESPACHAR
                      </button>
                    )}
                  </div>
                  <Link
                    to={`/admin/compras/${data._id}`}
                    className="text-blue-800 ml-auto mr-4"
                  >
                    Ver orden de compra
                  </Link>
                </div>
              );
            })}
          </div>
          <Paginate
            allProducts={ordenes.length}
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
};

export default PanelCompras;
