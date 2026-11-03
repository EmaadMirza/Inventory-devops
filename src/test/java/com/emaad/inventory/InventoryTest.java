package com.emaad.inventory;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class InventoryTest {
    @Test void createsAndListsProducts() {
        Inventory i = new Inventory(); var p=i.add("Notebook",10);
        assertEquals("Notebook",p.name()); assertEquals(10,i.list().get(0).stock());
    }
    @Test void updatesStockAndRejectsMissingProduct() {
        Inventory i=new Inventory(); var p=i.add("Pen",5);
        assertEquals(8,i.setStock(p.id(),8).stock());
        assertThrows(java.util.NoSuchElementException.class,()->i.setStock(999,1));
    }
    @Test void rejectsInvalidProductsAndStock() {
        Inventory i=new Inventory();
        assertThrows(IllegalArgumentException.class,()->i.add(" ",1));
        assertThrows(IllegalArgumentException.class,()->i.add("Pen",-1));
        var p=i.add("Pen",0);
        assertThrows(IllegalArgumentException.class,()->i.setStock(p.id(),-2));
        assertEquals(0,i.list().get(0).stock());
    }
}
