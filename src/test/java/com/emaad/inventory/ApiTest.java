package com.emaad.inventory;

import com.sun.net.httpserver.HttpServer;
import java.net.URI;
import java.net.http.*;
import java.util.concurrent.ExecutorService;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class ApiTest {
    private HttpServer server;
    private String base;
    private final HttpClient client = HttpClient.newHttpClient();
    @BeforeEach void start() throws Exception {
        server = App.start(0, new Inventory());
        base = "http://127.0.0.1:" + server.getAddress().getPort();
    }
    @AfterEach void stop() {
        server.stop(0);
        ((ExecutorService) server.getExecutor()).shutdownNow();
    }
    private HttpResponse<String> request(String method, String path, String json) throws Exception {
        return client.send(HttpRequest.newBuilder(URI.create(base + path))
            .header("Content-Type", "application/json")
            .method(method, HttpRequest.BodyPublishers.ofString(json)).build(),
            HttpResponse.BodyHandlers.ofString());
    }
    @Test void createsFindsAndUpdatesProductOverHttp() throws Exception {
        assertEquals(201, request("POST", "/products", "{\"name\":\"Pen\",\"stock\":2}").statusCode());
        var found = request("GET", "/products/1", "");
        assertEquals(200, found.statusCode());
        assertTrue(found.body().contains("Pen"));
        assertEquals(200, request("PUT", "/products/1/stock", "{\"stock\":8}").statusCode());
        assertTrue(request("GET", "/products/1", "").body().contains("\"stock\":8"));
        assertEquals(404, request("GET", "/products/999", "").statusCode());
        assertEquals(405, request("POST", "/products/1", "{}").statusCode());
    }
    @Test void rejectsMalformedFractionalNegativeAndOversizedInput() throws Exception {
        for (String body : new String[]{"{", "null", "[]", "{\"name\":null,\"stock\":1}",
            "{\"name\":\"Pen\",\"stock\":1.5}", "{\"name\":\"Pen\",\"stock\":-1}", " ".repeat(8193)}) {
            assertEquals(400, request("POST", "/products", body).statusCode(), body.substring(0, Math.min(80, body.length())));
        }
    }
    @Test void filtersLowStockWithoutChangingInventory() throws Exception {
        request("POST", "/products", "{\"name\":\"Pen\",\"stock\":2}");
        request("POST", "/products", "{\"name\":\"Notebook\",\"stock\":10}");
        var filtered = request("GET", "/products?maxStock=2", "");
        assertEquals(200, filtered.statusCode());
        assertTrue(filtered.body().contains("Pen"));
        assertFalse(filtered.body().contains("Notebook"));
        assertTrue(request("GET", "/products", "").body().contains("Notebook"));
        assertEquals(400, request("GET", "/products?maxStock=-1", "").statusCode());
    }
    @Test void reportsHealthAndRejectsUnknownRoute() throws Exception {
        assertEquals(200, request("GET", "/health", "").statusCode());
        assertEquals(404, request("GET", "/unknown", "").statusCode());
    }
}
