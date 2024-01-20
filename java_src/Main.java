import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.util.Collections;

public class Main {
    public static void main(String[] args) {
        //args format: argument: value (future implementation)
        String APIurl = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + args[0] + "&interval=5min&month=2023-12&outputsize=full&datatype=csv&apikey=ID65LPK90VSEGPLZ";
        String databaseURL = "jdbc:sqlite:output.db";

        try {
            URL url = new URL(APIurl); //string to url

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            int responseCode = connection.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;

                Class.forName("org.sqlite.JDBC");
                Connection dbConnection = DriverManager.getConnection(databaseURL);

                String headerline = in.readLine();
                if (headerline.equals("{}")) {
                    System.out.print("API Error");
                    System.exit(1);
                }
                System.out.print(headerline);
                String[] columnTitles = ("symbol," + headerline).split(",");

                StringBuilder sqlStatement = new StringBuilder("DROP TABLE IF EXISTS OUTPUT");
                dbConnection.createStatement().executeUpdate(sqlStatement.toString());
                sqlStatement = new StringBuilder("CREATE TABLE IF NOT EXISTS OUTPUT (");
                sqlStatement.append("id INTEGER PRIMARY KEY AUTOINCREMENT, ");
                for (String columnTitle : columnTitles) {
                    sqlStatement.append(columnTitle).append(" TEXT, ");
                }
                sqlStatement.setLength(sqlStatement.length()  -  2);
                sqlStatement.append(")");
                System.out.println(sqlStatement);

                dbConnection.createStatement().executeUpdate(sqlStatement.toString());
                String insertQuery = "INSERT INTO output (symbol, timestamp, open, high, low, close, volume) VALUES (" + repeat("?", columnTitles.length) + ")";
                System.out.println(insertQuery);
                PreparedStatement preparedStatement = dbConnection.prepareStatement(insertQuery);
            
                while ((inputLine = in.readLine()) != null){
                    String[] fields = (args[0] + ", " + inputLine).split(",");
                    for (int i  = 0; i < fields.length; i++) {
                        preparedStatement.setString(i + 1, fields[i]);
                    }
                    preparedStatement.executeUpdate();
                }
                preparedStatement.close();
                dbConnection.close();
            } else {
                System.out.println("API request failed.");
            }

            // Close the connection
            connection.disconnect();
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static String repeat(String str, int n) {
        return String.join(", ", Collections.nCopies(n, str));
    }
}