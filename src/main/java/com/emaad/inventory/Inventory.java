package com.emaad.inventory;
import java.util.*;

/** One process owns one inventory. State is intentionally not shared across replicas. */
public final class Inventory {
    public record Product(long id, String name, int stock) {}
    private final Map<Long, Product> products = new LinkedHashMap<>();
    private long nextId = 1;
    public synchronized Product add(String name, int stock) {
        if (name == null || name.isBlank() || stock < 0) throw new IllegalArgumentException("Name is required and stock must be nonnegative");
        Product p = new Product(nextId++, name.trim(), stock); products.put(p.id(), p); return p;
    }
    public synchronized List<Product> list() { return List.copyOf(products.values()); }
    public synchronized Product find(long id) {
        Product product = products.get(id);
        if (product == null) throw new NoSuchElementException("Product not found");
        return product;
    }
    public synchronized Product setStock(long id, int stock) {
        if (stock < 0) throw new IllegalArgumentException("Stock must be nonnegative");
        Product old = products.get(id);
        if (old == null) throw new NoSuchElementException("Product not found");
        Product updated = new Product(id, old.name(), stock); products.put(id, updated); return updated;
    }
}
