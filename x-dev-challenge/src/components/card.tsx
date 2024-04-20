

const card = () => {
    return (
        <div className={"flex flex-col items-center rounded-md shadow-sm shadow-white bg-zinc-700 m-2 p-1"}>
            <h1 className={"text-2xl text-white font-public-sans"}>
                Card Name
            </h1>
            <p className={"text-sm text-white font-public-sans"}>
                Card Description
            </p>
        </div>
    )
}

export default card