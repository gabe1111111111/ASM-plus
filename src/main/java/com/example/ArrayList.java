package com.example;

import java.util.Iterator;
/**
 * this class emulates the java ArrayList class.
 * only the necessary functions are implemented
 * @author Gabriel Lacey
 */
public class ArrayList<T> implements Iterable<T> {
    private T[] data;
    private  int size;
    /**
     * constructor initializes data and size
     */
    @SuppressWarnings("unchecked")
    public ArrayList() {
    data = (T[]) new Object[1];
    size = 0;
    }
    
    /**
     * adds addend to the array
     * @param addend what is getting added to the array
     */
    public void add(T addend){
        ensureCapacity(size+1);
        data[size] = addend;
        size++;
    }
    /**
     * if the data length is not already at least as long as the length
     * it will ensure the data length is either length or double the current size witch ever one is greater
     * @param length minimum length of the array
     */
    @SuppressWarnings({"unchecked", "ManualArrayToCollectionCopy"})
    private void ensureCapacity(int length){
        if(size >= length)return;
        int max = length;
        if(size*size > max)max = size*size;
        T[] temp = (T[])new Object[max];
        
        for(int i = 0; i < size; i++){
            temp[i] = data[i];
        }  

        data = temp;
    }
    /**
     * returns data[location]
     * @param location index of the array
     * @return data at location
     * @throws IndexOutOfBoundsException if location >= size of the array
     */
    public T get(int location)throws IndexOutOfBoundsException{
        
        if(location >= size) throw new IndexOutOfBoundsException();
        return data[location];
    }
    @Override
    public Iterator<T> iterator() {
        // TO DO Auto-generated method stub
        return new ArrayListIterator<>();
       // throw new UnsupportedOperationException("Unimplemented method 'iterator'");
    }
   /**
    * removes null objects from visible part of the array
    */
    @SuppressWarnings("unchecked")
    public void clean(){
        T[] temp = (T[])new Object[size];
        int newSize = 0;
        for(int i = 0; i < size; i++){
            if(data[i] != null) temp[newSize++] = data[i];
            
        
        }  
        size = newSize;
        data = temp;
    }
    /**
     * 
     * @param target what it is checking to contain
     * @return true if the array contains the target
     */
    public boolean contains(T target){
        int index = 0;
        for(T i : data){
            if(index >= size) break;
            if(i == target) return true;
            if(i.equals(target)) return true;
            index ++;
        }
        return false;
    }
    /**
     * this method is designed for map entries 
     * @param target what it is checking to contain
     * @param ignored used to overload the method
     * @return returns the target id it is contained and null otherwise
     */
    public T contains(T target, boolean ignored){
        int index = 0;
        for(T i : data){
            if(index >= size) break;
            if(i == target) return i;
            if(i.equals(target)) return i;
            index ++;
        }
        return null;
    }
    private class ArrayListIterator<E> implements Iterator<E>{
        private int current = -1;
        @Override
        public boolean hasNext() {
            // TO DO Auto-generated method stub
            if(current + 1 >= size) return false;

            return data[current + 1]  != null;
            //throw new UnsupportedOperationException("Unimplemented method 'hasNext'");
        }

        @SuppressWarnings("unchecked")
        @Override
        public E next() {
            // TO DO Auto-generated method stub
            current++;
            return (E)data[current];
            //throw new UnsupportedOperationException("Unimplemented method 'next'");
        }

       
    
        
    }
    /**
     * 
     * @return the number of elements stored
     */
    public int size(){
        return size;
    }
    /**
     *replaces the data at index with addend 
     * @param addend what to replace with 
     *@param index where to replace
     */
    public void replace(T addend, int index){
        if(index >= size)throw new IndexOutOfBoundsException();
        data[index] = addend;
    }
}