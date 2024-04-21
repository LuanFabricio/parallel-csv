use std::{
    fs,
    thread::{self, JoinHandle},
};

use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct Person {
    id: u32,
    name: String,
}

impl parallel_files::Format for Person {
    fn format(&self) -> String {
        format!("{},{}", self.id, self.name)
    }
}

fn main() {
    let files = vec![
        "assets/example/input/test1.json".to_string(),
        "assets/example/input/test2.json".to_string(),
    ];

    let mut thread_handler: Vec<JoinHandle<()>> = Vec::new();

    let mut i = 0;
    for file_json in files {
        i += 1;
        let handler = thread::spawn(move || {
            if let Ok(file_str) = fs::read_to_string(file_json.clone()) {
                let json: Vec<Person> = serde_json::from_str(&file_str).unwrap();
                parallel_files::write_into_csv(i, json)();
            }
        });
        thread_handler.push(handler);
    }

    for handler in thread_handler {
        let _ = handler.join();
    }
}
