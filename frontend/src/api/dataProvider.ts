import { DataProvider, fetchUtils } from "react-admin";
import { stringify } from "query-string";
import { API_URL } from "../constants";

const httpClient = fetchUtils.fetchJson;

const dataProvider: DataProvider = {
  /**
   *
   * @param resource => The url of where the resource is located
   * @param params =>
   *    pagination => {page: how many pages to fetch, perPage: how many entries per page}
   *    sort => {field: on which field to sort by, order: Ascending or Descending}
   *    fileter => {anyField: val} we can filter the data using any fields
   *
   * @returns => List of data
   */
  getList: (resource: string, params: any) => {
    const pagination = params.pagination || { page: 1, perPage: 10 };
    const { page, perPage } = pagination;

    const sort = params.sort || { field: "id", order: "ASC" };
    const { field, order } = sort;
    const query = {
      sort: JSON.stringify([field, order]),
      range: JSON.stringify([(page - 1) * perPage, page * perPage - 1]),
      filter: JSON.stringify(params.filter),
    };
    const url = `${API_URL}/${resource}?${stringify(query)}`;
    console.log(url);

    return httpClient(url).then(({ headers, json }) => ({
      data: json,
      // extract the total number of resources from the Content-Range header and return it as a number.
      // This number could then be used to determine the total number of pages in a paginated response
      // total: parseInt(headers.get('content-range')!.split('/').pop() as string, 10),
    }));
  },

  /**
   *
   * @param resource The url of where the resource is located
   * @param params
   *    id = val : any field of the table to fetch data
   * @returns => The particular data
   *
   * CHANGED => added `?id=` without adding it it is not working
   */
  getOne: (resource: string, params: any) =>
    httpClient(`${API_URL}/${resource}/?id=${params.id}`).then(({ json }) => ({
      data: json,
    })),

  /**
   *
   * @param resource The url of where the resource is located
   * @param params
   *      ids = [id1, id2, id3, ...]
   *
   * @returns List of data corresponding to the specified ids
   */
  getMany: (resource: string, params: any) => {
    const query = {
      filter: JSON.stringify({ ids: params.ids }),
    };
    // console.log(params.ids);
    const url = `${API_URL}/${resource}?${stringify(query)}`;
    return httpClient(url).then(({ json }) => ({ data: json }));
  },

  /**
   *
   * @param resource The url of where the resource is located
   * @param params
   *    pagination => {page: how many pages to fetch, perPage: how many entries per page}
   *    sort => {field: on which field to sort by, order: Ascending or Descending}
   *    fileter => {anyField: val} we can filter the data using any fields
   * @returns => Didn't understand what it does
   */
  getManyReference: (resource: string, params: any) => {
    const pagination = params.pagination || { page: 1, perPage: 10 };
    const { page, perPage } = pagination;

    const sort = params.sort || { field: "id", order: "ASC" };
    const { field, order } = sort;
    const query = {
      sort: JSON.stringify([field, order]),
      range: JSON.stringify([(page - 1) * perPage, page * perPage - 1]),
      filter: JSON.stringify({
        ...params.filter,
        [params.target!]: params.id,
      }),
    };
    const url = `${API_URL}/${resource}?${stringify(query)}`;

    return httpClient(url).then(({ headers, json }) => ({
      data: json,
      //   total: parseInt(
      //     headers.get("content-range")!.split("/").pop() as string,
      //     10
      //   ),
    }));
  },

  /**
   *
   * @param resource The url of where the resource is located
   * @param params
   *    Data with the corresponding fields to insert into the table
   * @returns
   *    Inserted object
   * 
   * DIDN'T TEST CUZ POST METHOD IS NOT IMPLEMENTED
   */
  create: (resource: string, params: any) => {
    // Make sure that the data property is present and of type object
    if (!params.data || typeof params.data !== "object") {
      throw new Error("Invalid data");
    }
    // Return a promise that resolves to an object with a data property
    return new Promise((resolve, reject) => {
      httpClient(`${API_URL}/${resource}`, {
        method: "POST",
        body: JSON.stringify(params.data),
      })
        .then(({ json }) => {
          resolve({ data: { ...params.data, id: json.id } });
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  /**
   *
   * @param resource The url of where the resource is located
   * @param params
   *    ID of the table (i.e PK)
   *    Data with the corresponding fields to insert into the table
   * @returns
   *    Nothing
   * 
   * DIDN'T TEST CUZ PUT METHOD IS NOT IMPLEMENTED
   */
  update: (resource: string, params: any) =>
    httpClient(`${API_URL}/${resource}/${params.id}`, {
      method: "PUT",
      body: JSON.stringify(params.data),
    }).then(({ json }) => ({ data: json })),

  /**
   *
   * @param resource The url of where the resource is located
   * @param params
   *    IDs of the table as [id1, id2, id3, ..] (i.e PK)
   *    Data with the corresponding fields to insert into the table
   * @returns
   *    Updated JSON response
   * 
   * DIDN'T TEST CUZ PUT METHOD IS NOT IMPLEMENTED
   */
  updateMany: (resource: string, params: any) => {
    const query = {
      filter: JSON.stringify({ id: params.ids }),
    };
    return httpClient(`${API_URL}/${resource}?${stringify(query)}`, {
      method: "PUT",
      body: JSON.stringify(params.data),
    }).then(({ json }) => ({ data: json }));
  },

  /**
   *
   * @param resource The url of where the resource is located
   * @param params
   *    IDs of the table as [id1, id2, id3, ..] (i.e PK)
   *    Data with the corresponding fields to insert into the table
   * @returns
   *    Nothing
   *
   * DIDN'T TEST CUZ DELETE METHOD IS NOT IMPLEMENTED
   */
  delete: (resource: string, params: any) =>
    httpClient(`${API_URL}/${resource}/${params.id}`, {
      method: "DELETE",
    }).then(({ json }) => ({ data: json })),

  /**
   *
   * @param resource The url of where the resource is located
   * @param params
   *    IDs of the table as [id1, id2, id3, ..] (i.e PK)
   *    Data with the corresponding fields to insert into the table
   * @returns
   * 
   * DIDN'T TEST CUZ DELETE METHOD IS NOT IMPLEMENTED
   */
  deleteMany: (resource: string, params: any) => {
    const query = {
      filter: JSON.stringify({ id: params.ids }),
    };
    return httpClient(`${API_URL}/${resource}?${stringify(query)}`, {
      method: "DELETE",
      body: JSON.stringify(params.data),
    }).then(({ json }) => ({ data: json }));
  },
};

export default dataProvider;
