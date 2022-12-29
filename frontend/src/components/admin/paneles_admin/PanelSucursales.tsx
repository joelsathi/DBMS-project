import { useEffect } from "react";
import { FaTrashAlt } from "react-icons/fa";
import { useNavigate } from "react-router";
import useHeaders from "../../../app/header";
import { useAppDispatch, useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";
import { borrarOffice } from "../../slices/admin";
import { fetchAllOffices } from "../../slices/offices";

const PanleSucuersales = () => {
  const token = JSON.parse(window.localStorage.getItem("token") || "{}");
  const header = useHeaders(token);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    dispatch(fetchAllOffices());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const deleteOffice = (e: any, id: string) => {
    window.location.reload();
    e.preventDefault();
    dispatch(borrarOffice(header.headers, id));
  };

  const data = useAppSelector((state: RootState) => state.offices);

  return (
    <div className="bg-white bg-admin-banner bg-no-repeat pt-20 pb-1  bg-contain">
      <h1 className="text-white justify-center py-20 mb-2 text-5xl font-bold flex align-middle items-center">
        PANEL DE SUCURSALES
      </h1>
      <div className=" m-8 bg-white border-2 px-4 border-black rounded-lg">
        <div className="flex justify-end m-5">
          <button
            onClick={() => navigate("/admin/offices/create")}
            className="bg-[#855C20] mr-4 py-2 px-2 text-white rounded-lg font-semibold"
          >
            CREAR BARBERIA
          </button>
        </div>

        <div className="relative">
          <div className="ml-12 grid grid-cols-[1fr_.2fr_.2fr_.2fr] w-[55%] pr-8 gap-16 justify-items-start">
            <p>Ubicacion</p>
            <p>Latitud</p>
            <p>Longitud</p>
          </div>
        </div>

        {data.allOffices?.map((office) => (
          <div
            className="m-5 grid grid-cols-4  gap-16 py-2 pl-2 mt-8 border border-black rounded-lg justify-items-start
              "
          >
            <h1>{office.location}</h1>
            <h1>{office.lat}</h1>
            <h1>{office.long}</h1>
            <FaTrashAlt
              className="cursor-pointer "
              title="Eliminar producto"
              onClick={(e) => {
                deleteOffice(e, office._id);
              }}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default PanleSucuersales;
