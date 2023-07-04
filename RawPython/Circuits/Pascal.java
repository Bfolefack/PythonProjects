import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Scanner;

public class Pascal {
    public static void main(String[] args) throws IOException{
        Scanner sc = new Scanner(new File("Pascal.dat"));
        while(sc.hasNextInt()){
            createTriangle(sc.nextInt());
        }
    }
    public static void createTriangle(int layers) {

        int[] pascal = {1};
        for(int i = 0; i < layers; i++){
            System.out.println(Arrays.toString(pascal));
            int[] nextPascal = new int[pascal.length + 1];
            nextPascal[0] = 1;
            nextPascal[nextPascal.length - 1] = 1;
            for(int j = 1; j < nextPascal.length - 1; j++){
                nextPascal[j] = pascal[j - 1] + pascal[j];
            }
            pascal = nextPascal;
        }
    }
}