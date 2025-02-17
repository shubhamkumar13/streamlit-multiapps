from nested_dict import nested_dict
import os


class BenchStruct:
    config = {}

    def __init__(self):
        self.structure = nested_dict(3, list)
        self.config["bench_type"] = "sequential"
        self.config["artifacts_dir"] = "/Users/shubham/sandmark-nightly"
        self.config["bench_stem"] = "_1.orun.summary.bench"
    
    def add(self, host, timestamp, commit, variant):
        self.structure[host][timestamp][commit].append(variant)
    
    def add_files(self, files):
        for x in files:
            l = x.split(str("/" + self.config["bench_type"] + "/"))[1]
            d = l.split("/")
            self.add(
                d[0],
                d[1],
                d[2],
                d[3]
            )
    
    def to_filepath(self):
        lst = []
        for host, timestamps in self.structure.items():
            for timestamp, commits in timestamps.items():
                for commit, bench_files in commits.items():
                    t = [self.config["artifacts_dir"] + "/" + self.config["bench_type"] + "/" + str(host) + "/" + str(timestamp) + "/" + str(commit) + "/" + str(bench_file) for bench_file in bench_files]
                    lst.append(t)
        return lst

    def get_bench_files(self):
        bench_files = []

        # Loads file metadata
        for root, dirs, files in os.walk(self.config["artifacts_dir"] + "/" + self.config["bench_type"]):
            for file in files:
                if file.endswith(self.config["bench_stem"]):
                    f = root.split("/" + self.config["bench_type"])
                    bench_files.append((os.path.join(root,file)))
        
        return bench_files


    def __repr__(self):
        return f'{self.structure}'