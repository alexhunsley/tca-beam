// MARK: - View

public struct {{ viewClass }}: View {

    private let store: StoreOf<AutoSuggestViewFeature>

    public init(
        store: StoreOf<AutoSuggestViewFeature>
    ) {
        self.store = store
    }

    public var body: some View {
        WithViewStore(store) { viewStore in
            // content here
        }
    }
}

// MARK: - Preview

public struct {{ viewClass }}_Preview: PreviewProvider {

    public static var previews: some View {
        {{ viewClass }}(store: StoreOf<{{ featureClass }}>(
                initialState: .init(),
                reducer: {{ featureClass }}()
            ))
        }
    }
}
