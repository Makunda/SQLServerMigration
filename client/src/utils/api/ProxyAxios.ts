import axios from 'axios';
import ApiResponseImpl from "./response/ApiResponseImpl";


export default class ProxyAxios {
  /**
   * Get the URL
   * @returns The URL of the api
   */
  public static getURl(): string {
    return `http://localhost:5000/api`;
  }

  /**
   * Get with Authentication
   * @param url Url to query
   * @param config (Optional) Configuration of the query
   * @returns A promise ending when the query is completed
   */
  public static async get<T>(
      url: string,
      config?: any,
  ): Promise<ApiResponseImpl<T>> {
    config = await this.buildConfig(config); // Create configuration
    url = this.buildUrl(url); // Append base url

    try {
      const response = await axios.get(url, config);
      return new ApiResponseImpl<T>(response);
    } catch (error) {
      const e = (error as any)
      if (e.response) {
        return new ApiResponseImpl<T>(e.response);
      }
      throw error;
    }
  }

  /**
   * Download a file as a blob
   * @param fileUrl Url of the file to download
   * @param type Type of file
   * @returns A Promise returning a blob with the type specified
   */
  public static async downloadFile(
      fileUrl: string,
      type: string,
  ): Promise<Blob> {
    const config = await this.buildConfig({ responseType: 'blob' }); // Create configuration
    const url = this.buildUrl(fileUrl); // Append base url

    return axios
        .get(url, config)
        .then((response) => new Blob([response.data], { type }))
        .catch((err: any) => {
          throw err;
        });
  }

  /**
   * Post with Authentication
   * @param url Url to query
   * @param data Data to send
   * @param config (Optional) Configuration to use
   * @returns A promise ending when the query is completed
   */
  public static async post<T>(
      url: string,
      data?: any,
      config?: any,
  ): Promise<ApiResponseImpl<T>> {
    config = await this.buildConfig(config); // Create configuration
    url = this.buildUrl(url); // Append base url

    try {
      const response = await axios.post(url, data, config);
      return new ApiResponseImpl<T>(response);
    } catch (error) {
      const e = (error as any)
      if (e.response) {
        return new ApiResponseImpl<T>(e.response);
      }
      throw error;
    }
  }

  /**
   * Put with Authentication
   * @param url Url to query
   * @param data Data to send
   * @param config (Optional) Configuration to use
   * @returns A promise ending when the query is completed
   */
  public static async put<T>(
      url: string,
      data: any,
      config?: any,
  ): Promise<ApiResponseImpl<T>> {
    config = await this.buildConfig(config); // Create configuration
    url = this.buildUrl(url); // Append base url

    try {
      const response = await axios.put(url, data, config);
      return new ApiResponseImpl<T>(response);
    } catch (error) {
      const e = (error as any)
      if (e.response) {
        return new ApiResponseImpl<T>(e.response);
      }
      throw error;
    }
  }

  /**
   * Delete with Authentication
   * @param url Url to query
   * @param body (Optional) Body to send
   * @param config (Optional) Configuration to use
   * @returns A promise ending when the query is completed
   */
  public static async delete<T>(
      url: string,
      body?: any,
      config?: any,
  ): Promise<ApiResponseImpl<T>> {
    config = await this.buildConfig(config); // Create configuration
    url = ProxyAxios.getURl() + url; // Append base url
    if (body) config.data = body;

    try {
      const response = await axios.delete(url, config);
      return new ApiResponseImpl<T>(response);
    } catch (error) {
      const e = (error as any)
      if (e.response) {
        return new ApiResponseImpl<T>(e.response);
      }
      throw error;
    }
  }

  /**
   * Get the base url
   * @param url Base url to the API
   * @private
   */
  private static buildUrl(url: string): string {
    return this.getURl() + url;
  }

  /**
   * *Build and return a config containing the header file
   * @param config The existing config
   * @returns Enriched configuration
   */
  private static async buildConfig(config?: any): Promise<any> {
    if (!config) config = {}; // Make sure the config isn't null


    return config;
  }
}

export class NewAxiosProxy extends ProxyAxios {}
