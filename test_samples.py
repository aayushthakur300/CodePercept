samples = {
    # ==============================================================================
    # 1. STANDARD BASELINE SAMPLES (Simple checks)
    # ==============================================================================
    "c": '#include <stdio.h>\nint main() { printf("Hello"); return 0; }',
    "cpp": '#include <iostream>\nusing namespace std;\nint main() { cout << "Hi"; }',
    "java": 'public class Test { public static void main(String[] args) { System.out.println("Hi"); } }',
    "javascript": 'function test() { console.log("JS"); }',
    "typescript": 'const msg: string = "TS"; interface A { x: number; }',
    "python": 'def test(x):\n    print(x)',
    "go": 'package main\nimport "fmt"\nfunc main() { fmt.Println("Hi") }',
    "rust": 'fn main() { println!("Hello"); }',
    "r": 'x <- 5\nprint(x)',
    "php": '<?php\necho "hello";\n?>',
    "perl": 'use strict;\nmy $x = 10;',
    "ruby": 'def hi\n  puts "hello"\nend',
    "swift": 'import Foundation\nfunc main() {}',
    "kotlin": 'fun main() { val x = 5 }',
    "dart": 'void main() { print("hi"); }',
    "matlab": 'function y = square(x)\n% comment\ny = x*x;',
    "sql": 'SELECT * FROM users;',
    "html": '<!doctype html>\n<html><body>Hello</body></html>',
    "css": 'body { color: red; }',
    "elixir": 'defmodule Test do\n  def hi do\n  end\nend',
    "csharp": 'using System;\nclass A { static void Main() { Console.WriteLine("Hi"); } }',

    # ==============================================================================
    # 2. THE TORTURE CHAMBER (Ambiguous Edge Cases)
    # ==============================================================================
    "javascript_ambiguous": 'console.log("hi");',
    "typescript_ambiguous": 'let x: number = 5;',
    "python_ambiguous": 'print("hello")',
    "sql_ambiguous": 'SELECT 1;',
    "c_ambiguous": '#include <stdio.h>\nint main() {}',
    "cpp_ambiguous": '#include <iostream>\nint main() { return 0; }',
    "java_ambiguous": 'class A { public static void main(String[] args) {} }',
    "csharp_ambiguous": 'Console.WriteLine("Hi");',
    "ruby_ambiguous": 'puts "hello"',
    "go_ambiguous": 'func main() {}',
    
    # ==============================================================================
    # 3. SPECIFIC CONFLICT TESTS (Tie-Breaker Logic)
    # ==============================================================================
    "r_tricky": 'x <- 5; df <- data.frame(a=1:5)', # Should be R, not Go
    "cpp_tricky": '#include <vector>\nint main() { return 0; }', # Should be C++, not C
    "matlab_tricky": 'A = [1 2; 3 4];', # Should be MATLAB, not Python
    "swift_guard": 'func test() { guard let x = y else { return } }', # Should be Swift
    "kotlin_data": 'data class User(val name: String)', # Should be Kotlin
    "elixir_pipe": 'data |> process()', # Should be Elixir

    # ==============================================================================
    # 4. COMPLEX REAL-WORLD TESTS (The "Supreme" Validation)
    # ==============================================================================
    
    # --- C Language ---
    "c_complex": """
    #include <stdio.h>
    #include <stdlib.h>
    
    typedef struct {
        int id;
        char *name;
    } User;

    void process(User *u) {
        if (u == NULL) return;
        printf("Processing ID: %d\\n", u->id);
    }

    int main() {
        User *u = (User *)malloc(sizeof(User));
        u->id = 1;
        process(u);
        free(u);
        return 0;
    }
    """,

    # --- C++ ---
    "cpp_complex": """
    #include <iostream>
    #include <vector>
    #include <algorithm>
    #include <map>

    using namespace std;

    template <typename T>
    class Processor {
    public:
        void run(const vector<T>& data) {
            for (const auto& item : data) {
                cout << item << endl;
            }
        }
    };

    int main() {
        vector<int> v = {1, 2, 3, 4};
        Processor<int> p;
        p.run(v);
        return 0;
    }
    """,

    # --- Java ---
    "java_complex": """
    package com.example.demo;

    import java.util.List;
    import java.util.stream.Collectors;
    import java.util.ArrayList;

    public class UserManager {
        public static void main(String[] args) {
            List<String> names = new ArrayList<>();
            names.add("Alice");
            names.add("Bob");
            
            List<String> filtered = names.stream()
                .filter(n -> n.startsWith("A"))
                .collect(Collectors.toList());
                
            System.out.println(filtered);
        }
    }
    """,

    # --- C# ---
    "csharp_complex": """
    using System;
    using System.Linq;
    using System.Collections.Generic;

    namespace DemoApp {
        public class User {
            public int Id { get; set; }
            public string Name { get; set; }
        }

        class Program {
            static void Main(string[] args) {
                var users = new List<User> { new User { Id = 1, Name = "Test" } };
                var query = from u in users
                            where u.Id > 0
                            select u.Name;
                            
                foreach (var name in query) {
                    Console.WriteLine($"User: {name}");
                }
            }
        }
    }
    """,

    # --- Python ---
    "python_complex": """
    import os
    from datetime import datetime

    def logger_decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper

    class DataProcessor:
        def __init__(self, data):
            self.data = [x for x in data if x % 2 == 0]

        @logger_decorator
        def process(self):
            with open("log.txt", "w") as f:
                f.write(str(self.data))
    
    if __name__ == "__main__":
        dp = DataProcessor(range(10))
        dp.process()
    """,

    # --- JavaScript (UPDATED) ---
    "javascript_complex": """
    const processData = (data) => {
        let results = [];
        data.forEach(item => {
            if (item.active) {
                // Object spread syntax
                results.push({ ...item, processed: true });
            }
        });
        console.log("Processing complete");
        return results;
    };

    // CommonJS export makes it distinct from TS/ESM ambiguity
    module.exports = { processData };
    """,

    # --- TypeScript (UPDATED) ---
    "typescript_complex": """
    interface User {
        id: number;
        email: string;
        role?: 'admin' | 'user';
    }

    // Class implementing an interface
    class UserService implements IService<User> {
        private users: User[] = [];

        public addUser(user: User): void {
            this.users.push(user);
        }

        public getUser(id: number): User | undefined {
            return this.users.find(u => u.id === id);
        }
    }
    """,

    # --- Go ---
    "go_complex": """
    package main

    import (
        "fmt"
        "sync"
    )

    type Worker struct {
        ID int
    }

    func (w *Worker) Process(ch chan int, wg *sync.WaitGroup) {
        defer wg.Done()
        for job := range ch {
            fmt.Printf("Worker %d processing %d\\n", w.ID, job)
        }
    }

    func main() {
        ch := make(chan int, 10)
        var wg sync.WaitGroup
        
        wg.Add(1)
        w := Worker{ID: 1}
        go w.Process(ch, &wg)
        
        ch <- 1
        close(ch)
        wg.Wait()
    }
    """,

    # --- Rust ---
    "rust_complex": """
    use std::collections::HashMap;

    struct Processor {
        cache: HashMap<String, i32>,
    }

    impl Processor {
        fn new() -> Self {
            Processor { cache: HashMap::new() }
        }

        fn process(&mut self, key: &str) -> Option<&i32> {
            match self.cache.get(key) {
                Some(val) => Some(val),
                None => {
                    println!("Key not found");
                    None
                }
            }
        }
    }

    fn main() {
        let mut p = Processor::new();
        p.process("test");
    }
    """,

    # --- PHP ---
    "php_complex": """
    <?php
    namespace App\\Controllers;

    use App\\Models\\User;

    class UserController extends BaseController {
        private $db;

        public function __construct(Database $db) {
            $this->db = $db;
        }

        public function index(Request $request) {
            $users = User::where('active', 1)->get();
            foreach ($users as $user) {
                echo "User: " . $user->name;
            }
            return response()->json(['status' => 'ok']);
        }
    }
    """,

    # --- Ruby ---
    "ruby_complex": """
    require 'json'

    module App
        class Processor
            attr_accessor :data

            def initialize(data)
                @data = data
            end

            def process!
                @data.map do |item|
                    item.upcase
                end
            end
        end
    end

    5.times do |i|
        puts "Processing #{i}"
    end
    """,

    # --- Swift ---
    "swift_complex": """
    import Foundation
    import UIKit

    struct User: Codable {
        let id: Int
        let name: String
    }

    class NetworkManager {
        func fetchUser(completion: @escaping (Result<User, Error>) -> Void) {
            guard let url = URL(string: "https://api.test.com") else { return }
            
            URLSession.shared.dataTask(with: url) { data, _, _ in
                if let data = data {
                    print("Received data");
                }
            }.resume()
        }
    }
    """,

    # --- Kotlin ---
    "kotlin_complex": """
    data class User(val id: Int, val name: String)

    object Repository {
        private val users = mutableListOf<User>()

        fun addUser(user: User) {
            users.add(user)
        }

        fun findUser(name: String): User? {
            return users.find { it.name == name }?.also {
                println("Found user: $it")
            }
        }
    }

    fun main() {
        val user = User(1, "Kotlin")
        Repository.addUser(user)
    }
    """,

    # --- Dart ---
    "dart_complex": """
    import 'dart:async';
    import 'package:http/http.dart' as http;

    class ApiService {
        Future<void> fetchData() async {
            try {
                final response = await http.get(Uri.parse('url'));
                if (response.statusCode == 200) {
                    print('Success');
                }
            } catch (e) {
                print('Error: $e');
            }
        }
    }

    void main() async {
        final service = ApiService();
        await service.fetchData();
    }
    """,

    # --- R ---
    "r_complex": """
    library(dplyr)
    library(ggplot2)

    data <- data.frame(
        id = 1:10,
        value = rnorm(10)
    )

    result <- data %>%
        filter(value > 0) %>%
        mutate(category = ifelse(value > 1, "High", "Low")) %>%
        group_by(category) %>%
        summarise(mean_val = mean(value))

    ggplot(result, aes(x=category, y=mean_val)) +
        geom_bar(stat="identity")
    """,

    # --- MATLAB ---
    "matlab_complex": """
    a = [3,7,2,9,3,7,8,3,10,4,6,7,2,9,5,3,7,8,6,4];
    a = sort(a);
    n = numel(a);
    meanv = mean(a);
    if mod(n,2)==1
        medianv = a((n+1)/2);
    else
        medianv = (a(n/2)+a(n/2+1))/2;
    end
    vals = unique(a);
    freq = zeros(size(vals));
    for i = 1:numel(vals)
        freq(i) = sum(a==vals(i));
    end
    [~,idx] = max(freq);
    modev = vals(idx);
    varv = sum((a-meanv).^2)/n;
    sdv = sqrt(varv);
    fprintf("Count: %d\\n",n);
    fprintf("Min: %d Max: %d\\n",a(1),a(end));
    fprintf("Mean: %.3f Median: %.3f Mode: %d\\n",meanv,medianv,modev);
    fprintf("StdDev: %.3f\\n",sdv);
    for i = 1:numel(vals)
        fprintf("%d: %s\\n",vals(i),repmat('*',1,freq(i)));
    end
    """ ,
    
    # --- Perl ---
    "perl_complex": """
    use strict;
    use warnings;

    sub process_file {
        my ($filename) = @_;
        open(my $fh, '<', $filename) or die "Could not open file '$filename' $!";
        
        while (my $row = <$fh>) {
            chomp $row;
            if ($row =~ m/^Error:\s*(.*)/) {
                print "Found error: $1\\n";
            }
        }
        close $fh;
    }

    my %config = ( debug => 1, retries => 3 );
    process_file("log.txt");
    """,

    # --- SQL ---
    "sql_complex": """
    SELECT 
        u.id, 
        u.email, 
        COUNT(o.id) as order_count,
        SUM(o.total) as total_spent
    FROM users u
    JOIN orders o ON u.id = o.user_id
    WHERE o.created_at > '2023-01-01'
    GROUP BY u.id, u.email
    HAVING COUNT(o.id) > 5
    ORDER BY total_spent DESC;
    """,

    # --- HTML ---
    "html_complex": """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Complex Page</title>
        <script src="app.js" defer></script>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <div id="app">
            <header class="main-header">
                <nav>
                    <ul><li><a href="#">Home</a></li></ul>
                </nav>
            </header>
            <main>
                <article>Content here</article>
            </main>
        </div>
    </body>
    </html>
    """,

    # --- CSS ---
    "css_complex": """
    :root {
        --primary-color: #2563eb;
        --spacing: 1rem;
    }

    body {
        margin: 0;
        font-family: system-ui, sans-serif;
        background-color: #f0f0f0;
    }

    .container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: var(--spacing);
    }

    @media (max-width: 768px) {
        .sidebar {
            display: none;
        }
    }

    .btn:hover {
        background-color: rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    """,

    # --- Elixir ---
    "elixir_complex": """
    defmodule MathProcessor do
      def process(list) do
        list
        |> Enum.filter(fn x -> rem(x, 2) == 0 end)
        |> Enum.map(fn x -> x * 2 end)
        |> Enum.sum()
      end

      def handle_message({:ok, msg}) do
        IO.puts("Received: #{msg}")
      end

      def handle_message({:error, _reason}) do
        IO.puts("Error occurred")
      end
    end
    """,

    # ==============================================================================
    # 5. REGRESSION TESTS (The Fixes)
    # ==============================================================================
    # 1. C
    "c_regression": """
    #include <stdio.h>
    #include <stdlib.h>
    int main() {
        int *ptr = (int*)malloc(sizeof(int));
        *ptr = 10;
        printf("Value: %d", *ptr);
        free(ptr);
        return 0;
    }
    """,

    # 2. C++
    "cpp_regression": """
    #include <vector>
    #include <iostream>
    using namespace std;
    int main() {
        vector<int> v = {1, 2, 3};
        for(auto i : v) cout << i << endl;
        return 0;
    }
    """,

    # 3. Java
    "java_regression": """
    import java.util.HashMap;
    public class Test {
        public static void main(String[] args) {
            HashMap<String, Integer> map = new HashMap<>();
            map.put("key", 1);
            System.out.println(map.get("key"));
        }
    }
    """,

    # 4. C#
    "csharp_regression": """
    using System;
    public class Program {
        public static void Main() {
            Console.WriteLine("Hello C#");
            var x = new { Name = "Test" };
        }
    }
    """,

    # 5. Python (Standard + List Comp)
    "python_regression": """
    import sys
    data = [x*2 for x in range(10) if x > 5]
    def run():
        print(f"Data: {data}")
    if __name__ == "__main__":
        run()
    """,

    # 6. JavaScript
    "javascript_regression": """
    const process = (items) => {
        items.forEach(item => console.log(item));
        return items.map(i => i * 2);
    };
    export default process;
    """,

    # 7. TypeScript
    "typescript_regression": """
    interface User {
        id: number;
        name: string;
    }
    const getUser = (u: User): void => {
        console.log(u.name);
    }
    """,

    # 8. Go
    "go_regression": """
    package main
    import "fmt"
    func main() {
        ch := make(chan int)
        go func() { ch <- 42 }()
        val := <-ch
        fmt.Println(val)
    }
    """,

    # 9. Rust
    "rust_regression": """
    fn main() {
        let x = vec![1, 2, 3];
        match x.get(0) {
            Some(v) => println!("Value: {}", v),
            None => println!("None"),
        }
    }
    """,

    # 10. PHP
    "php_regression": """
    <?php
    function test($var) {
        return "Value: " . $var;
    }
    $arr = [1, 2, 3];
    foreach ($arr as $v) { echo test($v); }
    """,

    # 11. Ruby
    "ruby_regression": """
    class Greeter
      attr_accessor :name
      def initialize(name)
        @name = name
      end
      def say_hi
        puts "Hi #{@name}"
      end
    end
    Greeter.new("Ruby").say_hi
    """,

    # 12. Perl
    "perl_regression": """
    use strict;
    use warnings;
    my @array = (1, 2, 3);
    foreach my $i (@array) {
        print "Index: $i\n";
    }
    sub hello { print "Hello"; }
    """,

    # 13. Swift
    "swift_regression": """
    import Foundation
    func greet(name: String?) {
        guard let n = name else { return }
        print("Hello \(n)")
    }
    greet(name: "Swift")
    """,

    # 14. Kotlin
    "kotlin_regression": """
    data class User(val id: Int)
    fun main() {
        val u = User(1)
        println("User ID: ${u.id}")
    }
    """,

    # 15. Dart
    "dart_regression": """
    void main() {
        List<String> list = ['a', 'b'];
        list.forEach((item) {
            print('Item: $item');
        });
    }
    """,

    # 16. R (Standard + Bug Fix Case)
    "r_regression": """
    data <- c(1, 2, 3, 4)
    mean_val <- mean(data)
    print(paste("Mean:", mean_val))
    # Bug fix check (semicolons/print)
    a=3; b=9
    print(a+b)
    """,

    # 17. MATLAB (Standard + Bug Fix Case)
    "matlab_regression": """
    % Matrix operations
    A = zeros(3, 3);
    for i = 1:3
        A(i,i) = 1;
    end
    disp(A);
    % Bug fix check (semicolon usage)
    x = 4; y = 12;
    disp(x+y)
    """,

    # 18. SQL
    "sql_regression": """
    SELECT u.name, COUNT(o.id) 
    FROM users u 
    LEFT JOIN orders o ON u.id = o.user_id 
    GROUP BY u.name 
    HAVING COUNT(o.id) > 5;
    """,

    # 19. HTML
    "html_regression": """
    <!DOCTYPE html>
    <html lang="en">
    <body>
        <div id="app"><h1>Hello</h1></div>
        <script>console.log('test');</script>
    </body>
    </html>
    """,

    # 20. CSS
    "css_regression": """
    .container {
        display: flex;
        justify-content: center;
        background-color: #f0f0f0;
    }
    @media (max-width: 600px) {
        .container { flex-direction: column; }
    }
    """,

    # 21. Elixir
    "elixir_regression": """
    defmodule Tester do
      def run(list) do
        list
        |> Enum.map(fn x -> x * 2 end)
        |> IO.inspect()
      end
    end
    """
}