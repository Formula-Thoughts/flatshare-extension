import { Axios, AxiosInstance, AxiosResponse } from "axios";
import axios from "./axios";

export const _getGroupById = async (id: string) => {
  const res = (await axios.get(`/groups/${id}`)) as AxiosResponse;
  return res.data;
};

export const _getUserGroup = async (token: string) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const res = (await axios.get(`/groups`, config)) as AxiosResponse;
  return res.data;
};

export const _createGroup = async (token: string) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const res = (await axios.post(`/groups`, {}, config)) as AxiosResponse;
  return res.data;
};

export const _addFlat = async (
  groupCode: string,
  url: string,
  price: string,
  title: string
) => {
  const body = {
    url,
    price,
    title,
  };
  const res = (await axios.post(
    `/groups/${groupCode}/flats`,
    body
  )) as AxiosResponse;
  return res.data;
};

export const _deleteFlat = async (groupCode: string, flatId: string) => {
  const res = (await axios.delete(
    `/groups/${groupCode}/flats/${flatId}`
  )) as AxiosResponse;
  return res.data;
};

export const _getGroupShareCode = async (id: string) => {
  const res = (await axios.get(`/groups/${id}/code`)) as AxiosResponse;
  return res.data;
};
