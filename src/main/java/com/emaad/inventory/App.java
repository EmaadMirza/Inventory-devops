package com.emaad.inventory;
import com.google.gson.*;
import com.sun.net.httpserver.*;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.*;

public final class App {
    private static final Gson JSON = new Gson();
    private static final int MAX_BODY = 8192;
    public static HttpServer start(int port, Inventory inventory) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", port), 32);
        server.setExecutor(new ThreadPoolExecutor(2, 4, 30, TimeUnit.SECONDS,
            new ArrayBlockingQueue<>(64), new ThreadPoolExecutor.CallerRunsPolicy()));
        server.createContext("/", exchange -> {
            try {
                String path = exchange.getRequestURI().getPath();
                String method = exchange.getRequestMethod();
                if (path.equals("/health")) {
                    if (!method.equals("GET")) { send(exchange,405,Map.of("error","Use GET")); return; }
                    send(exchange,200,Map.of("status","UP","instance",System.getenv().getOrDefault("HOSTNAME","local")));
                } else if (path.equals("/products")) {
                    if (method.equals("GET")) send(exchange,200,inventory.list());
                    else if (method.equals("POST")) {
                        JsonObject body = readBody(exchange);
                        if (!body.has("name") || !body.get("name").isJsonPrimitive() || !body.getAsJsonPrimitive("name").isString()) throw new IllegalArgumentException("name must be a string");
                        send(exchange,201,inventory.add(body.get("name").getAsString(),stock(body)));
                    } else send(exchange,405,Map.of("error","Use GET or POST"));
                } else if (path.matches("/products/[0-9]+")) {
                    if (!method.equals("GET")) { send(exchange,405,Map.of("error","Use GET")); return; }
                    send(exchange,200,inventory.find(Long.parseLong(path.split("/")[2])));
                } else if (path.matches("/products/[0-9]+/stock")) {
                    if (!method.equals("PUT")) { send(exchange,405,Map.of("error","Use PUT")); return; }
                    long id = Long.parseLong(path.split("/")[2]);
                    send(exchange,200,inventory.setStock(id,stock(readBody(exchange))));
                } else send(exchange,404,Map.of("error","Not found"));
            } catch (NoSuchElementException e) { send(exchange,404,Map.of("error",e.getMessage())); }
              catch (IllegalArgumentException | JsonParseException | ArithmeticException e) { send(exchange,400,Map.of("error","Invalid JSON or product data")); }
              catch (Exception e) { send(exchange,500,Map.of("error","Internal server error")); }
            finally { exchange.close(); }
        });
        server.start(); return server;
    }
    private static JsonObject readBody(HttpExchange exchange) throws IOException {
        byte[] bytes = exchange.getRequestBody().readNBytes(MAX_BODY + 1);
        if (bytes.length > MAX_BODY) throw new IllegalArgumentException("Request too large");
        JsonElement parsed = JsonParser.parseString(new String(bytes, StandardCharsets.UTF_8));
        if (!parsed.isJsonObject()) throw new IllegalArgumentException("Expected JSON object");
        return parsed.getAsJsonObject();
    }
    private static int stock(JsonObject body) {
        JsonElement value = body.get("stock");
        if (value == null || !value.isJsonPrimitive() || !value.getAsJsonPrimitive().isNumber()) throw new IllegalArgumentException("stock must be an integer");
        return value.getAsBigDecimal().intValueExact();
    }
    private static void send(HttpExchange exchange, int status, Object body) throws IOException {
        byte[] bytes = JSON.toJson(body).getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type","application/json; charset=utf-8");
        exchange.sendResponseHeaders(status,bytes.length); exchange.getResponseBody().write(bytes);
    }
    public static void main(String[] args) throws Exception {
        Inventory inventory = new Inventory(); inventory.add("Notebook",10); inventory.add("Pen",25);
        int port = Integer.parseInt(System.getenv().getOrDefault("APP_PORT","8080"));
        HttpServer server = start(port,inventory);
        Runtime.getRuntime().addShutdownHook(new Thread(() -> { server.stop(1); ((ExecutorService)server.getExecutor()).shutdownNow(); }));
        System.out.println("Mini Inventory API listening on " + port);
    }
}
