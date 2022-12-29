import { useState } from "react";
import useHeaders from "../../app/header";
import { useAppDispatch } from "../../app/hooks";
import { comprar } from "../slices/purchaseOrder";

export interface input {
  nombre: string;
  apellido: string;
  email: string;
  direccionEnvio: string;
  localidad: string;
  CP: number;
  tel: string;
}

const CrearProducto = () => {
  const dispatch = useAppDispatch();
  const user: any = JSON.parse(window.localStorage.getItem("user") || "[]");
  const token = JSON.parse(window.localStorage.getItem("token") || "{}");
  const header = useHeaders(token);
  const products: any = JSON.parse(
    window.localStorage.getItem("product") || "[]"
  );
  const compra = products?.map((productos: any) => {
    return {
      price: productos.productos.price,
      cantidad: productos.cantidad,
      name: productos.productos.name,
    };
  });
  // if(user.google_account) {const nombre = user.name.split('')}

  const [nom, ap] = user.google_account
    ? user.name.split(" ")
    : [user.name, user.lastname];

  const [inputs, setInputs] = useState<input>({
    nombre: user.google_account ? nom : user.name,
    apellido: user.google_account ? ap : user.lastname,
    email: user.email,
    tel: user.tel,
    direccionEnvio: user.adress,
    localidad: user.localidad,
    CP: user.CD,
  });

  const [errors, setErrors] = useState<any>({});


  //================handlers===========
  const handleInput = (e: React.ChangeEvent<any>) => {
    setInputs((prevState) => ({
      ...prevState,
      [e.target.name]: e.target.value,
    }));
  };

  const clearState = () => {
    setInputs(() => {
      return {
        nombre: "",
        apellido: "",
        email: "",
        direccionEnvio: "",
        localidad: "",
        CP: 0,
        tel: "",
      };
    });
  };

  const handleSubmit = () => {
    dispatch(comprar(header.headers, laCompra));
    clearState();
  };

  const laCompra = {
    user: inputs,
    compra,
  };

  //===================render========================//
  return (
    <div className="flex bg-bg-prods bg-cover">
      <div className="  lg:w-[40%] lg:mx-auto mx-4 my-16 py-8 px-8 bg-white/50 rounded-lg">
        <h1 className="text-lg  flex ">
          Por favor llene los campos para finalizar su compra
        </h1>
        <div className="lg:grid flex flex-col grid-cols-2 my-16 gap-y-8">
          <div className="lg:block flex flex-col">
            <label htmlFor="nombre">Nombre: </label>
            <input
              value={inputs.nombre}
              type="text"
              name="nombre"
              onChange={(e) => handleInput(e)}
              className="rounded-lg bg-white/70 pl-4"
            />
          </div>
          <div className="lg:block flex flex-col">
            <label htmlFor="apellido">Apellido: </label>
            <input
              value={inputs.apellido}
              type="text"
              name="apellido"
              onChange={(e) => handleInput(e)}
              className="rounded-lg bg-white/70 pl-4"
            />
          </div>
          <div className="col-span-2 flex flex-col">
            <label htmlFor="email">Email: </label>
            <input
              value={inputs.email}
              type="text"
              name="email"
              onChange={(e) => handleInput(e)}
              className="rounded-lg bg-white/70 pl-4"
            />
          </div>
          <div className="col-span-2 flex flex-col">
            <label htmlFor="email">Telefono: </label>
            <input
              value={inputs.tel}
              type="text"
              name="tel"
              onChange={(e) => handleInput(e)}
              className="rounded-lg bg-white/70 pl-4"
            />
          </div>
          <div className="col-span-2 flex flex-col">
            <label htmlFor="direccionEnvio">Direccion de envio: </label>
            <input
              value={inputs.direccionEnvio}
              type="text"
              name="direccionEnvio"
              onChange={(e) => handleInput(e)}
              className="rounded-lg bg-white/70 pl-4"
            />
          </div>

          <div>
            <label htmlFor="localidad">Localidad: </label>
            <input
              value={inputs.localidad}
              type="text"
              name="localidad"
              onChange={(e) => handleInput(e)}
              className="rounded-lg bg-white/70 pl-4"
            />
          </div>

          <div className="flex lg:flex-row flex-col">
            <label htmlFor="precio">CP: </label>
            <input
              value={inputs.CP}
              type="text"
              minLength={4}
              maxLength={4}
              name="CP"
              onChange={(e) => handleInput(e)}
              className="rounded-lg bg-white/70 pl-4 flex ml-2 flex-col"
            />
          </div>
        </div>

        <button
          onClick={() => {
            handleSubmit();
          }}
          className="lg:flex justify-self-end bg-black text-white lg:w-[20%] block rounded-sm p-4 ml-auto "
        >
          FINALIZAR COMPRA
        </button>
      </div>
    </div>
  );
};

export default CrearProducto;
