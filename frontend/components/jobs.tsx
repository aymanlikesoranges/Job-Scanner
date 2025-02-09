"use clienlt"

interface Job {
    job: string,
    link: string,
    company: string,
    posted: string,
    location: string,
}

export function Jobs({jobs}: {jobs: Job[]}) {
    return (<div className="overflow-x-auto">
        <table className="table">
            <thead>
                <tr>
                    <th>Job</th>
                    <th>Company</th>
                    <th>Posted</th>
                    <th>Location</th>
                    <th>Apply</th>
                </tr>
            </thead>
            <tbody>
                {jobs.map(job =>
                    <tr key={job.link}>
                        <td>{job.job}</td>
                        <td>{job.company}</td>
                        <td>{job.posted}</td>
                        <td>{job.location}</td>
                        <td><a className="link link-primary" href={job.link}>🚀 Apply</a></td>
                    </tr>
                )}
            </tbody>
        </table>
    </div >)
}