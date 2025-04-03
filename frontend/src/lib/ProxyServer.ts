export class ProxyServer {

    // TODO (Team 12 - Jorge): Move to a ResponseManager and RequestManager class
    requestHistory: string[] = [];
    responseHistory: string[] = [];

    async sendRequest(requestConfig: {
        url: string;
        method: string;
        headers?: Record<string, string>; // Optional parameters for sending
        body?: string;
        cookies?: string;
        params?: string;
    }): Promise<string> {
        const { url, method, headers = {}, body, cookies, params } = requestConfig;

        this.requestHistory.push(`${method} ${url}`);

        try {
            const proxyUrl = `http://localhost:8000/proxy`; //Proxy with localhost backend
            const payload = {
                url,
                method,
                headers,
                body,
                cookies,
                params
            };

            const response = await fetch(proxyUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            const data = await response.text();
            this.responseHistory.push(data);
            return data;

        } catch (error) {
            console.error("Error sending request:", error);
            this.responseHistory.push("Error fetching data.");
            return "Error fetching data.";
        }
    }

    getHistory() {
        return {
            requests: this.requestHistory,
            responses: this.responseHistory
        };
    }
}

export class HTTPClient {
    proxy: ProxyServer;
    log: string[] = []; //TODO: Move to logger class
    results: Record<string, string> = {};

    constructor(proxy: ProxyServer) {
        this.proxy = proxy;
    }

    //General method for sending
    async sendRequestToProxy(config): Promise<string> {
        this.log.push(`Sending ${config.method} request to ${config.url}`);
        const result = await this.proxy.sendRequest(config);
        this.results[config.url] = result;
        return result;
    }

    getLogs(): string[] {
        return this.log;
    }

    getResults(): Record<string, string> {
        return this.results;
    }
}
