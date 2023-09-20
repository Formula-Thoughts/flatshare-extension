export interface FlatImageProps {
  id: string;
  name: string;
  image: string;
}

function FlatImage(props: { item: FlatImageProps }) {
  const { item } = props;
  console.log("item", item);
  return <img width={30} height={30} src={item.image} alt="Web Page" />;
}

export default FlatImage;
