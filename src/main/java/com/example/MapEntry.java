package com.example;
/**
 * this class emulates the java MapEntry class.
 * only the necessary functions are implemented
 * @author Gabriel Lacey
 */
public class MapEntry<T, U> {
    public T  key;
    public U value;
    /**
     * 
     * @param key this is what gets compared
     * @param value this is the data identifiable by the key
     */
    public MapEntry(T key, U value) {
        this.key = key; 
        this.value = value;
    }
    /**
     * @return weather or not the keys are equal 
    */
    @SuppressWarnings("unchecked")
    @Override
    public boolean equals(Object obj) {
        if(obj.getClass() == MapEntry.class)
            return(key.equals(((MapEntry<T, U>) obj).key));
        return key.equals(obj);
    }
    
}
