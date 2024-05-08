import { useState } from "react";
import { useLocation } from "react-router-dom";
import ColorLayout from "./layouts/ColorLayout";
import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en";
TimeAgo.addDefaultLocale(en);

type Data = {
  flatUrl: string;
};

type WarningType = {
  data: string;
  votes: string[];
  added: Date;
};

const Warnings = () => {
  const location = useLocation();
  const data: Data = location.state;

  const [warnings] = useState<WarningType[]>([
    {
      data: "“We went to see this property and it had mould all over the place, stay away!”",
      votes: ["user_id", "user_id_2"],
      added: new Date(),
    },
  ]);

  return (
    <ColorLayout>
      <div>Warnings {JSON.stringify(data.flatUrl)}</div>
      {warnings.map((warning) => {
        return <Warning {...warning} />;
      })}
    </ColorLayout>
  );
};

const Warning = (props: WarningType) => {
  const timeAgo = new TimeAgo("en-US");

  return (
    <div>
      <p>"{JSON.stringify(props.data)}"</p>
      <p>"{props.votes.length} users agree"</p>
      <p>{timeAgo.format(props.added)}</p>
    </div>
  );
};

export default Warnings;
