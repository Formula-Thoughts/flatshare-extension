import { AxiosResponse } from "axios";
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
  try {
    const res = (await axios.get(`/groups`, config)) as AxiosResponse;
    return res.data;
  } catch (err) {
    // console.log("err 401", err);
    throw err;
  }
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

export const _updateGroup = async (
  token: string,
  groupId: string,
  priceLimit: number,
  locations: string[]
) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const res = (await axios.put(
    `/groups/${groupId}`,
    {
      price_limit: Number(priceLimit),
      locations: locations,
    },
    config
  )) as AxiosResponse;
  return res.data;
};

export const _addFlat = async (
  token: string,
  groupCode: string,
  url: string,
  price: string | number,
  title: string
) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const res = (await axios.post(
    `/groups/${groupCode}/properties`,
    {
      url,
      price,
      title,
    },
    config
  )) as AxiosResponse;
  return res.data;
};

export const _deleteFlat = async (
  token: string,
  groupId: string,
  flatId: string
) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const res = (await axios.delete(
    `/groups/${groupId}/properties/${flatId}`,
    config
  )) as AxiosResponse;
  return res.data;
};

export const _getGroupShareCode = async (token: string, id: string) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const res = (await axios.get(`/groups/${id}/code`, config)) as AxiosResponse;
  return res.data;
};

export const _getPropertyRedFlags = async (
  token: string,
  propertyUrl: string
) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
  const res = (await axios.get(
    `/red-flags?property_url=${propertyUrl}`,
    config
  )) as AxiosResponse;
  return res.data;
};

export const _addRedFlag = async (
  token: string,
  propertyUrl: string,
  body: string
) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const res = (await axios.post(
    `/red-flags?property_url=${propertyUrl}`,
    {
      propertyUrl,
      body,
    },
    config
  )) as AxiosResponse;
  return res.data;
};

export const _voteRedFlag = async (
  token: string,
  redFlagId: string,
  propertyUrl: string,
  hasUserVoted: boolean
) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  let res = null;

  if (hasUserVoted) {
    // unvote

    const res = (await axios.delete(
      `/red-flags/${redFlagId}/votes?property_url=${propertyUrl}`,
      config
    )) as AxiosResponse;

    return res.data;
  } else {
    // vote
    res = (await axios.post(
      `/red-flags/${redFlagId}/votes?property_url=${propertyUrl}`,
      {},
      config
    )) as AxiosResponse;
    return res.data;
  }
};
